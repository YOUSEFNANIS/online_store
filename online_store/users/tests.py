from rest_framework.test import APITestCase

from .models import User, seller, customer

GOOD_PASSWORD = 'Str0ng!pass'


def make_customer(first='Cus', last='Tomer', password=GOOD_PASSWORD):
    user = User.objects.create_user(username=f'{first}_{last}', password=password,
                                    first_name=first, last_name=last, email=f'{first}@x.com')
    return customer.objects.create(user=user, phone_number='0911111111')


def make_seller(first='Sel', last='Ler', store='Shop', password=GOOD_PASSWORD):
    user = User.objects.create_user(username=f'{first}_{last}', password=password,
                                    first_name=first, last_name=last, email=f'{first}@x.com')
    return seller.objects.create(user=user, store_name=store, phone_number='0922222222')


class SignupTests(APITestCase):
    payload = {'first_name': 'Ali', 'last_name': 'Ahmed', 'email': 'ali@x.com',
               'password': GOOD_PASSWORD, 'phone_number': '0911111111'}

    def test_signup_is_open(self):
        response = self.client.post('/signup/customer/', self.payload)
        self.assertEqual(response.status_code, 201, response.content)

    def test_weak_password_rejected(self):
        response = self.client.post('/signup/customer/', {**self.payload, 'password': 'weak'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('password', response.json())

    def test_duplicate_names_get_unique_usernames(self):
        self.assertEqual(self.client.post('/signup/customer/', self.payload).status_code, 201)
        second = self.client.post('/signup/customer/', {**self.payload, 'email': 'ali2@x.com'})
        self.assertEqual(second.status_code, 201, second.content)
        self.assertEqual(User.objects.filter(first_name='Ali').count(), 2)


class AccountPermissionTests(APITestCase):
    def setUp(self):
        self.cust = make_customer()
        self.other_cust = make_customer('Oth', 'Er')
        self.sell = make_seller()

    def test_anonymous_cannot_list_or_retrieve(self):
        self.assertIn(self.client.get('/signup/seller/').status_code, (401, 403))
        self.assertIn(self.client.get(f'/signup/seller/{self.sell.id}/').status_code, (401, 403))

    def test_customer_cannot_list_sellers_or_customers(self):
        self.client.force_authenticate(self.cust.user)
        self.assertEqual(self.client.get('/signup/seller/').status_code, 403)
        self.assertEqual(self.client.get('/signup/customer/').status_code, 403)

    def test_customer_cannot_read_other_account(self):
        self.client.force_authenticate(self.cust.user)
        self.assertEqual(self.client.get(f'/signup/seller/{self.sell.id}/').status_code, 403)
        self.assertEqual(self.client.get(f'/signup/customer/{self.other_cust.id}/').status_code, 403)

    def test_owner_can_read_own_account(self):
        self.client.force_authenticate(self.cust.user)
        self.assertEqual(self.client.get(f'/signup/customer/{self.cust.id}/').status_code, 200)

    def test_staff_can_list(self):
        staff = User.objects.create_user(username='staff', password=GOOD_PASSWORD, is_staff=True)
        self.client.force_authenticate(staff)
        self.assertEqual(self.client.get('/signup/seller/').status_code, 200)


class SellerDirectoryTests(APITestCase):
    def setUp(self):
        self.cust = make_customer()
        self.sell = make_seller()

    def test_customer_sees_only_public_fields(self):
        self.client.force_authenticate(self.cust.user)
        response = self.client.get('/signup/sellers/')
        self.assertEqual(response.status_code, 200)
        row = response.json()['results'][0]
        self.assertEqual(set(row), {'id', 'store_name', 'store_image', 'product_count', 'rating_avg', 'rating_count'})

    def test_seller_and_anonymous_denied(self):
        self.assertIn(self.client.get('/signup/sellers/').status_code, (401, 403))
        self.client.force_authenticate(self.sell.user)
        self.assertEqual(self.client.get('/signup/sellers/').status_code, 403)

    def test_detail_includes_product_count(self):
        from core.models import product
        product.objects.create(name='P', price=5, seller=self.sell, inventory=1)
        self.client.force_authenticate(self.cust.user)
        response = self.client.get(f'/signup/sellers/{self.sell.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['product_count'], 1)

    def test_products_filter_by_seller(self):
        from core.models import product
        other = make_seller('Oth', 'Er', 'Other')
        product.objects.create(name='Mine', price=5, seller=self.sell, inventory=1)
        product.objects.create(name='Theirs', price=5, seller=other, inventory=1)
        self.client.force_authenticate(self.cust.user)
        response = self.client.get('/core/products/', {'seller': self.sell.id})
        self.assertEqual([p['name'] for p in response.json()['results']], ['Mine'])
