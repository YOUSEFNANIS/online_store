from decimal import Decimal

from rest_framework.test import APITestCase

from users.tests import make_customer, make_seller
from . import models


def make_product(seller, name='Item', price=10, inventory=5):
    return models.product.objects.create(name=name, price=price, seller=seller, inventory=inventory)


def fill_cart(customer, *pairs):
    cart = models.cart.objects.create(customer=customer)
    for product, quantity in pairs:
        models.cart_item.objects.create(cart=cart, product=product, quantity=quantity)


class CheckoutTests(APITestCase):
    def setUp(self):
        self.cust = make_customer()
        self.s1 = make_seller('One', 'Seller', 'Store1')
        self.s2 = make_seller('Two', 'Seller', 'Store2')
        self.client.force_authenticate(self.cust.user)

    def test_checkout_decrements_stock_and_records_pending(self):
        p = make_product(self.s1, inventory=5)
        fill_cart(self.cust, (p, 2))
        response = self.client.post('/core/orders/', {'location': 'Tripoli'})
        self.assertEqual(response.status_code, 201, response.content)
        p.refresh_from_db()
        self.assertEqual(p.inventory, 3)
        body = response.json()
        self.assertEqual(body['order_status'], 'pending')
        self.assertEqual([e['status'] for e in body['status_history']], ['pending'])

    def test_checkout_rejects_insufficient_stock(self):
        p = make_product(self.s1, inventory=1)
        fill_cart(self.cust, (p, 2))
        response = self.client.post('/core/orders/', {'location': 'Tripoli'})
        self.assertEqual(response.status_code, 400)
        p.refresh_from_db()
        self.assertEqual(p.inventory, 1)
        self.assertEqual(models.order.objects.count(), 0)

    def test_cart_with_two_sellers_makes_two_orders(self):
        fill_cart(self.cust, (make_product(self.s1, 'A', 10), 1), (make_product(self.s2, 'B', 20), 1))
        self.assertEqual(self.client.post('/core/orders/', {'location': 'Tripoli'}).status_code, 201)
        totals = {o.seller_id: o.total_value for o in models.order.objects.all()}
        self.assertEqual(totals, {self.s1.id: Decimal('10'), self.s2.id: Decimal('20')})


class OrderLifecycleTests(APITestCase):
    def setUp(self):
        self.cust = make_customer()
        self.sell = make_seller()
        self.product = make_product(self.sell, price=50, inventory=5)
        fill_cart(self.cust, (self.product, 2))
        self.client.force_authenticate(self.cust.user)
        self.order_id = self.client.post('/core/orders/', {'location': 'Tripoli'}).json()['id']
        self.url = f'/core/orders/{self.order_id}/'

    def patch_as(self, user, status):
        self.client.force_authenticate(user)
        return self.client.patch(self.url, {'order_status': status}, format='json')

    def test_happy_path_credits_seller_on_delivery(self):
        self.assertEqual(self.patch_as(self.sell.user, 'confirmed').status_code, 200)
        self.assertEqual(self.patch_as(self.sell.user, 'shipped').status_code, 200)
        self.sell.refresh_from_db()
        self.assertEqual(self.sell.balance, 0)
        response = self.patch_as(self.cust.user, 'delivered')
        self.assertEqual(response.status_code, 200, response.content)
        self.sell.refresh_from_db()
        self.assertEqual(self.sell.balance, Decimal('95'))  # 100 sale - 5% commission
        self.assertEqual([e['status'] for e in response.json()['status_history']],
                         ['pending', 'confirmed', 'shipped', 'delivered'])

    def test_role_and_order_rules(self):
        self.assertEqual(self.patch_as(self.cust.user, 'confirmed').status_code, 400)
        self.assertEqual(self.patch_as(self.cust.user, 'delivered').status_code, 400)
        self.assertEqual(self.patch_as(self.sell.user, 'shipped').status_code, 400)
        self.assertEqual(self.patch_as(self.sell.user, 'delivered').status_code, 400)

    def test_cancel_restores_stock(self):
        self.assertEqual(self.patch_as(self.cust.user, 'cancelled').status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.inventory, 5)

    def test_final_state_is_locked(self):
        self.patch_as(self.cust.user, 'cancelled')
        self.assertEqual(self.patch_as(self.sell.user, 'confirmed').status_code, 405)

    def test_each_change_messages_the_other_side(self):
        from messaging.models import Message
        before = Message.objects.count()
        self.patch_as(self.sell.user, 'confirmed')
        self.assertEqual(Message.objects.count(), before + 1)
        self.assertIn('confirmed', Message.objects.latest('id').body)

    def test_allowed_transitions_shown_per_role(self):
        self.client.force_authenticate(self.sell.user)
        self.assertEqual(self.client.get(self.url).json()['allowed_transitions'], ['confirmed', 'cancelled'])
        self.client.force_authenticate(self.cust.user)
        self.assertEqual(self.client.get(self.url).json()['allowed_transitions'], ['cancelled'])
