from rest_framework.test import APITestCase

from users.tests import make_customer, make_seller
from .tests import fill_cart, make_product


def deliver(client, customer, seller, product, quantity=1):
    """Run a real order through checkout and the full status flow."""
    fill_cart(customer, (product, quantity))
    client.force_authenticate(customer.user)
    order_id = client.post('/core/orders/', {'location': 'Tripoli'}).json()['id']
    for user, status in ((seller.user, 'confirmed'), (seller.user, 'shipped'), (customer.user, 'delivered')):
        client.force_authenticate(user)
        client.patch(f'/core/orders/{order_id}/', {'order_status': status}, format='json')


class ReviewTests(APITestCase):
    def setUp(self):
        self.cust = make_customer()
        self.sell = make_seller()
        self.product = make_product(self.sell, inventory=10)
        self.url = f'/core/products/{self.product.id}/reviews/'

    def test_cannot_review_before_delivery(self):
        self.client.force_authenticate(self.cust.user)
        response = self.client.post(self.url, {'rating': 5, 'text': 'great'})
        self.assertEqual(response.status_code, 403)
        self.assertFalse(self.client.get(self.url + 'mine/').json()['can_review'])

    def test_review_after_delivery_updates_average_once(self):
        deliver(self.client, self.cust, self.sell, self.product)
        self.client.force_authenticate(self.cust.user)
        self.assertTrue(self.client.get(self.url + 'mine/').json()['can_review'])
        self.assertEqual(self.client.post(self.url, {'rating': 4, 'text': 'good'}).status_code, 201)
        self.assertEqual(self.client.post(self.url, {'rating': 5}).status_code, 400)
        detail = self.client.get(f'/core/products/{self.product.id}/').json()
        self.assertEqual((detail['rating_avg'], detail['rating_count']), (4.0, 1))

    def test_rating_bounds(self):
        deliver(self.client, self.cust, self.sell, self.product)
        self.client.force_authenticate(self.cust.user)
        self.assertEqual(self.client.post(self.url, {'rating': 6}).status_code, 400)
        self.assertEqual(self.client.post(self.url, {'rating': 0}).status_code, 400)

    def test_only_owner_can_edit_and_anyone_can_read(self):
        deliver(self.client, self.cust, self.sell, self.product)
        self.client.force_authenticate(self.cust.user)
        review_id = self.client.post(self.url, {'rating': 3}).json()['id']
        other = make_customer('Oth', 'Er')
        self.client.force_authenticate(other.user)
        self.assertEqual(self.client.patch(f'{self.url}{review_id}/', {'rating': 1}).status_code, 403)
        self.client.force_authenticate(None)
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_seller_rating_shows_in_directory(self):
        deliver(self.client, self.cust, self.sell, self.product)
        self.client.force_authenticate(self.cust.user)
        self.client.post(self.url, {'rating': 5})
        row = self.client.get('/signup/sellers/').json()['results'][0]
        self.assertEqual((row['rating_avg'], row['rating_count']), (5.0, 1))


class ReportTests(APITestCase):
    def setUp(self):
        self.cust = make_customer()
        self.sell = make_seller()
        self.product = make_product(self.sell)

    def test_report_product_and_duplicate_blocked(self):
        self.client.force_authenticate(self.cust.user)
        payload = {'product': self.product.id, 'reason': 'spam', 'details': 'fake listing'}
        self.assertEqual(self.client.post('/core/reports/', payload).status_code, 201)
        self.assertEqual(self.client.post('/core/reports/', payload).status_code, 400)

    def test_needs_exactly_one_target_and_login(self):
        anonymous = self.client.post('/core/reports/', {'product': self.product.id, 'reason': 'spam'})
        self.assertIn(anonymous.status_code, (401, 403))
        self.client.force_authenticate(self.cust.user)
        self.assertEqual(self.client.post('/core/reports/', {'reason': 'spam'}).status_code, 400)
        both = {'product': self.product.id, 'seller': self.sell.id, 'reason': 'spam'}
        self.assertEqual(self.client.post('/core/reports/', both).status_code, 400)

    def test_cannot_report_own_store(self):
        self.client.force_authenticate(self.sell.user)
        response = self.client.post('/core/reports/', {'seller': self.sell.id, 'reason': 'spam'})
        self.assertEqual(response.status_code, 400)
