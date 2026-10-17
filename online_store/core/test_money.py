from decimal import Decimal

from django.db.models import Sum
from rest_framework.test import APITestCase

from users.tests import make_customer, make_seller
from . import ledger, models
from .test_trust import deliver
from .tests import make_product


def ledger_total(seller):
    return models.LedgerEntry.objects.filter(seller=seller).aggregate(t=Sum('amount'))['t'] or Decimal('0')


class DeliveryMoneyTests(APITestCase):
    def setUp(self):
        self.cust = make_customer()
        self.sell = make_seller()

    def test_delivery_records_sale_and_commission_and_marks_paid(self):
        product = make_product(self.sell, price=50, inventory=10)
        deliver(self.client, self.cust, self.sell, product, quantity=4)  # total 200, 5% commission = 10
        order = models.order.objects.get()
        self.assertEqual((order.payment_method, order.payment_status), ('cod', 'paid'))
        kinds = {e.kind: e.amount for e in models.LedgerEntry.objects.filter(order=order)}
        self.assertEqual(kinds, {'sale': Decimal('200.00'), 'commission': Decimal('-10.00')})
        self.sell.refresh_from_db()
        self.assertEqual(self.sell.balance, Decimal('190'))
        self.assertEqual(self.sell.balance, ledger_total(self.sell))

    def test_cancelled_order_stays_unpaid_and_earns_nothing(self):
        product = make_product(self.sell, price=50, inventory=10)
        from .tests import fill_cart
        fill_cart(self.cust, (product, 1))
        self.client.force_authenticate(self.cust.user)
        order_id = self.client.post('/core/orders/', {'location': 'Tripoli'}).json()['id']
        self.client.patch(f'/core/orders/{order_id}/', {'order_status': 'cancelled'}, format='json')
        self.assertEqual(models.order.objects.get().payment_status, 'unpaid')
        self.assertEqual(models.LedgerEntry.objects.count(), 0)


class PayoutTests(APITestCase):
    def setUp(self):
        self.sell = make_seller()

    def give(self, amount):
        ledger.add_entry(self.sell.pk, ledger.ADJUSTMENT, Decimal(amount))

    def test_pays_everything_when_above_threshold(self):
        self.give('120.50')
        payouts = ledger.run_weekly_payouts()
        self.assertEqual(len(payouts), 1)
        self.assertEqual((payouts[0].amount, payouts[0].status), (Decimal('120.50'), 'paid'))
        self.sell.refresh_from_db()
        self.assertEqual(self.sell.balance, 0)
        self.assertEqual(self.sell.balance, ledger_total(self.sell))
        self.assertTrue(models.LedgerEntry.objects.filter(kind='payout', amount=Decimal('-120.50')).exists())

    def test_exactly_threshold_or_less_is_not_paid(self):
        self.give('100')
        self.assertEqual(ledger.run_weekly_payouts(), [])
        self.sell.refresh_from_db()
        self.assertEqual(self.sell.balance, Decimal('100'))

    def test_running_twice_pays_once(self):
        self.give('150')
        self.assertEqual(len(ledger.run_weekly_payouts()), 1)
        self.assertEqual(ledger.run_weekly_payouts(), [])
        self.assertEqual(models.Payout.objects.count(), 1)

    def test_only_sellers_above_threshold_are_paid(self):
        other = make_seller('Oth', 'Er', 'Other')
        self.give('300')
        ledger.add_entry(other.pk, ledger.ADJUSTMENT, Decimal('40'))
        paid = ledger.run_weekly_payouts()
        self.assertEqual([p.seller_id for p in paid], [self.sell.pk])


class EarningsApiTests(APITestCase):
    def setUp(self):
        self.sell = make_seller()
        self.other = make_seller('Oth', 'Er', 'Other')
        self.cust = make_customer()
        ledger.add_entry(self.sell.pk, ledger.ADJUSTMENT, Decimal('25'))
        ledger.add_entry(self.other.pk, ledger.ADJUSTMENT, Decimal('77'))

    def test_seller_sees_only_own_entries_and_summary(self):
        # add_entry updates balance in DB via F(); reload so the cached seller isn't stale.
        self.client.force_authenticate(type(self.sell.user).objects.get(pk=self.sell.user_id))
        rows = self.client.get('/core/earnings/').json()['results']
        self.assertEqual([r['amount'] for r in rows], ['25.00'])
        summary = self.client.get('/core/earnings/summary/').json()
        self.assertEqual(Decimal(summary['balance']), Decimal('25'))
        self.assertEqual(Decimal(summary['threshold']), Decimal('100'))
        self.assertIn('next_payout', summary)

    def test_customers_and_anonymous_denied(self):
        self.assertIn(self.client.get('/core/earnings/').status_code, (401, 403))
        self.client.force_authenticate(self.cust.user)
        self.assertEqual(self.client.get('/core/earnings/summary/').status_code, 403)
