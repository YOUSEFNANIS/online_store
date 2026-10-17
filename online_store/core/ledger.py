"""Seller money: every change to a seller's balance is a LedgerEntry, so balance == sum of entries."""
from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from . import models

SALE, COMMISSION, PAYOUT, ADJUSTMENT = 'sale', 'commission', 'payout', 'adjustment'


def add_entry(seller_id, kind, amount, order=None, payout=None):
    models.LedgerEntry.objects.create(seller_id=seller_id, kind=kind, amount=amount, order=order, payout=payout)
    models.seller.objects.filter(pk=seller_id).update(balance=F('balance') + amount)


def commission_for(total):
    return (Decimal(total) * Decimal(settings.COMMISSION_RATE)).quantize(Decimal('0.01'), ROUND_HALF_UP)


def record_delivery(order):
    """Cash on delivery: the courier collected the money, so the sale counts once the order is delivered."""
    add_entry(order.seller_id, SALE, order.total_value, order=order)
    fee = commission_for(order.total_value)
    if fee:
        add_entry(order.seller_id, COMMISSION, -fee, order=order)


def send_money(payout):
    """Demo transfer: no bank or wallet is called, the money is treated as sent immediately."""
    payout.status = 'paid'
    payout.paid_at = timezone.now()
    payout.save(update_fields=['status', 'paid_at'])


@transaction.atomic
def pay_out_seller(seller_id):
    seller = models.seller.objects.select_for_update().get(pk=seller_id)
    if seller.balance <= settings.PAYOUT_THRESHOLD:
        return None
    amount = seller.balance.quantize(Decimal('0.01'))
    payout = models.Payout.objects.create(seller=seller, amount=amount)
    add_entry(seller.pk, PAYOUT, -amount, payout=payout)
    send_money(payout)
    return payout


def run_weekly_payouts():
    """Pay every seller whose balance is above the threshold. Safe to run twice: a paid seller has 0 left."""
    due = models.seller.objects.filter(balance__gt=settings.PAYOUT_THRESHOLD).values_list('pk', flat=True)
    return [p for p in (pay_out_seller(pk) for pk in due) if p]
