from decimal import Decimal

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase

from users.tests import make_customer, make_seller
from . import models
from .test_trust import deliver
from .tests import make_product


def csv_file(text, name='products.csv'):
    return SimpleUploadedFile(name, text.encode('utf-8'), content_type='text/csv')


class StatsTests(APITestCase):
    def setUp(self):
        self.cust = make_customer()
        self.sell = make_seller()
        self.client.force_authenticate(self.sell.user)

    def test_revenue_top_products_and_low_stock(self):
        hot = make_product(self.sell, 'Hot', price=50, inventory=20)
        make_product(self.sell, 'Scarce', price=5, inventory=2)
        deliver(self.client, self.cust, self.sell, hot, quantity=3)  # revenue 150
        self.client.force_authenticate(self.sell.user)
        data = self.client.get('/core/seller/stats/').json()
        self.assertEqual(Decimal(str(data['revenue_30'])), Decimal('150'))
        self.assertEqual(data['orders_by_status'], {'delivered': 1})
        self.assertEqual([(t['name'], t['units']) for t in data['top_products']], [('Hot', 3)])
        self.assertEqual([p['name'] for p in data['low_stock']], ['Scarce'])

    def test_seller_only(self):
        self.client.force_authenticate(self.cust.user)
        for url in ('/core/seller/stats/', '/core/seller/export/orders/', '/core/seller/export/earnings/'):
            self.assertEqual(self.client.get(url).status_code, 403, url)
        self.client.force_authenticate(None)
        self.assertIn(self.client.get('/core/seller/stats/').status_code, (401, 403))


class ExportTests(APITestCase):
    def setUp(self):
        self.sell = make_seller()
        self.cust = make_customer('=cmd', 'Evil')  # name that would run as a spreadsheet formula
        self.product = make_product(self.sell, price=10, inventory=5)

    def test_orders_csv_has_rows_and_neutralises_formulas(self):
        deliver(self.client, self.cust, self.sell, self.product)
        self.client.force_authenticate(self.sell.user)
        response = self.client.get('/core/seller/export/orders/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/csv', response['Content-Type'])
        body = response.content.decode('utf-8-sig')
        lines = body.strip().splitlines()
        self.assertEqual(lines[0], 'order_id,date,customer,status,payment,location,total,items')
        self.assertEqual(len(lines), 2)
        self.assertIn("'=cmd Evil", lines[1])
        self.assertNotIn(',=cmd', lines[1])

    def test_only_own_orders_exported(self):
        other = make_seller('Oth', 'Er', 'Other')
        deliver(self.client, self.cust, other, make_product(other, 'Theirs'))
        self.client.force_authenticate(self.sell.user)
        body = self.client.get('/core/seller/export/orders/').content.decode('utf-8-sig')
        self.assertEqual(len(body.strip().splitlines()), 1)  # header only


class ImportTests(APITestCase):
    url = '/core/seller/import/products/'

    def setUp(self):
        self.sell = make_seller()
        self.cust = make_customer()
        self.cat = models.Category.objects.get_or_create(slug='t-imp', defaults={'name_en': 'Imp', 'name_ar': 'ا'})[0]
        self.client.force_authenticate(self.sell.user)

    def test_valid_file_creates_products_for_this_seller(self):
        text = f'name,description,price,inventory,category\nMug,Nice,12.50,10,{self.cat.slug}\nCap,,8,3,\n'
        response = self.client.post(self.url, {'file': csv_file(text)}, format='multipart')
        self.assertEqual(response.status_code, 201, response.content)
        self.assertEqual(response.json()['created'], 2)
        mug = models.product.objects.get(name='Mug')
        self.assertEqual((mug.seller, mug.category, mug.price), (self.sell, self.cat, Decimal('12.50')))

    def test_one_bad_row_creates_nothing(self):
        text = 'name,price,inventory\nGood,5,1\nBad,abc,1\nAlso bad,5,x\n'
        response = self.client.post(self.url, {'file': csv_file(text)}, format='multipart')
        self.assertEqual(response.status_code, 400)
        self.assertEqual([e['line'] for e in response.json()['errors']], [3, 4])
        self.assertEqual(models.product.objects.count(), 0)

    def test_unknown_category_and_missing_columns(self):
        bad_cat = self.client.post(self.url, {'file': csv_file('name,price,inventory,category\nA,5,1,nope\n')}, format='multipart')
        self.assertEqual(bad_cat.status_code, 400)
        missing = self.client.post(self.url, {'file': csv_file('name,price\nA,5\n')}, format='multipart')
        self.assertEqual(missing.status_code, 400)
        self.assertIn('inventory', missing.json()['detail'])

    def test_no_file_and_customers_denied(self):
        self.assertEqual(self.client.post(self.url, {}, format='multipart').status_code, 400)
        self.client.force_authenticate(self.cust.user)
        response = self.client.post(self.url, {'file': csv_file('name,price,inventory\nA,5,1\n')}, format='multipart')
        self.assertEqual(response.status_code, 403)
