from django.db import transaction
from django.db.models import F
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from . import ledger, models

PENDING = 'pending'
CONFIRMED = 'confirmed'
SHIPPED = 'shipped'
DELIVERED = 'delivered'
CANCELLED = 'cancelled'

FINAL_STATUSES = (DELIVERED, CANCELLED)

# role -> current status -> statuses that role may move the order to
TRANSITIONS = {
    'seller': {PENDING: [CONFIRMED, CANCELLED], CONFIRMED: [SHIPPED, CANCELLED]},
    'customer': {PENDING: [CANCELLED], SHIPPED: [DELIVERED]},
}


def owner_of(user):
    """Return (role, seller or customer id) for the user.

    CookieJWTAuthentication annotates seller_pk / customer_pk on the user, so this costs no query.
    Other authentication paths fall back to id-only lookups, cached on the user object.
    """
    if not hasattr(user, 'seller_pk'):
        user.seller_pk = models.seller.objects.filter(user_id=user.id).values_list('id', flat=True).first()
        user.customer_pk = None if user.seller_pk else (
            models.customer.objects.filter(user_id=user.id).values_list('id', flat=True).first())
    if user.seller_pk:
        return 'seller', user.seller_pk
    if user.customer_pk:
        return 'customer', user.customer_pk
    return None, None


def role_of(user):
    return owner_of(user)[0]


def allowed_transitions(role, status):
    return TRANSITIONS.get(role, {}).get(status, [])


def notify(order, actor, text):
    """Post a system line in the customer/seller conversation so the other side sees it in Messages."""
    if order.customer_id is None:
        return
    from messaging import models as chat
    conversation, _ = chat.Conversation.objects.get_or_create(customer=order.customer, seller=order.seller)
    chat.Message.objects.create(conversation=conversation, sender=actor, body=text)
    conversation.last_message_at = timezone.now()
    conversation.save(update_fields=['last_message_at'])


@transaction.atomic
def change_status(order_id, new_status, user):
    order = models.order.objects.select_for_update().select_related('seller', 'customer').get(pk=order_id)
    role = role_of(user)

    if new_status not in allowed_transitions(role, order.order_status):
        raise ValidationError({'order_status': f'Cannot change an order from {order.order_status} to {new_status}.'})

    if new_status == CANCELLED:
        for item in order.order_item_set.all():
            models.product.objects.filter(pk=item.product_id).update(inventory=F('inventory') + item.quantity)
    elif new_status == DELIVERED:
        order.payment_status = 'paid'  # cash on delivery: collected by the courier
        ledger.record_delivery(order)

    order.order_status = new_status
    order.save(update_fields=['order_status', 'payment_status'])
    models.OrderStatusEvent.objects.create(order=order, status=new_status, actor_role=role)
    notify(order, user, f'Order #{order.id} is now {new_status}.')
    return order
