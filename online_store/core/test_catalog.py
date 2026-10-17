from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from PIL import Image
from rest_framework.test import APITestCase

from users.tests import make_customer, make_seller
from . import models
from .tests import make_product

def png_bytes():
    buffer = BytesIO()
    Image.new('RGB', (2, 2), 'red').save(buffer, format='PNG')
    return buffer.getvalue()


class CategoryTests(APITestCase):
    def setUp(self):
        self.cust = make_customer()
        self.sell = make_seller()
        self.phones = models.Category.objects.get_or_create(slug='t-phones', defaults={'name_en': 'Phones', 'name_ar': 'هواتف'})[0]
        self.books = models.Category.objects.get_or_create(slug='t-books', defaults={'name_en': 'Books', 'name_ar': 'كتب'})[0]

    def test_categories_are_public(self):
        response = self.client.get('/core/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue({'t-phones', 't-books'} <= {c['slug'] for c in response.json()})

    def test_seller_sets_category_and_list_filters_by_it(self):
        self.client.force_authenticate(self.sell.user)
        created = self.client.post('/core/products/', {'name': 'Phone', 'price': '9.50', 'inventory': 3,
                                                       'category': self.phones.id}, format='json')
        self.assertEqual(created.status_code, 201, created.content)
        other = make_product(self.sell, 'Novel')
        other.category = self.books
        other.save()
        self.client.force_authenticate(self.cust.user)
        names = [p['name'] for p in self.client.get('/core/products/', {'category': self.phones.id}).json()['results']]
        self.assertEqual(names, ['Phone'])

    def test_related_prefers_same_category_and_skips_self_and_sold_out(self):
        main = make_product(self.sell, 'Main')
        main.category = self.phones
        main.save()
        same = make_product(self.sell, 'Same')
        same.category = self.phones
        same.save()
        sold_out = make_product(self.sell, 'SoldOut', inventory=0)
        sold_out.category = self.phones
        sold_out.save()
        response = self.client.get(f'/core/products/{main.id}/related/')
        self.assertEqual(response.status_code, 200)
        names = [p['name'] for p in response.json()]
        self.assertIn('Same', names)
        self.assertNotIn('Main', names)
        self.assertNotIn('SoldOut', names)


@override_settings(MEDIA_ROOT='/tmp/shop-test-media')
class ImagePermissionTests(APITestCase):
    def setUp(self):
        self.owner = make_seller()
        self.other = make_seller('Oth', 'Er', 'Other')
        self.cust = make_customer()
        self.product = make_product(self.owner)
        self.url = f'/core/products/{self.product.id}/images/'

    def upload(self):
        return self.client.post(self.url, {'image': SimpleUploadedFile('a.png', png_bytes(), content_type='image/png')},
                                format='multipart')

    def test_owner_can_upload_then_delete(self):
        self.client.force_authenticate(self.owner.user)
        created = self.upload()
        self.assertEqual(created.status_code, 201, created.content)
        image_id = created.json()['id']
        self.assertEqual(self.client.delete(f'{self.url}{image_id}/').status_code, 204)

    def test_others_cannot_change_images(self):
        self.assertIn(self.upload().status_code, (401, 403))
        self.client.force_authenticate(self.cust.user)
        self.assertEqual(self.upload().status_code, 403)
        self.client.force_authenticate(self.other.user)
        self.assertEqual(self.upload().status_code, 403)


class WishlistTests(APITestCase):
    def setUp(self):
        self.cust = make_customer()
        self.sell = make_seller()
        self.product = make_product(self.sell)

    def test_add_is_idempotent_and_listed(self):
        self.client.force_authenticate(self.cust.user)
        for _ in range(2):
            self.assertEqual(self.client.post('/core/wishlist/', {'product': self.product.id}).status_code, 201)
        self.assertEqual(models.WishlistItem.objects.count(), 1)
        self.assertEqual(self.client.get('/core/wishlist/ids/').json(), [self.product.id])
        results = self.client.get('/core/wishlist/').json()['results']
        self.assertEqual([p['id'] for p in results], [self.product.id])

    def test_remove(self):
        self.client.force_authenticate(self.cust.user)
        self.client.post('/core/wishlist/', {'product': self.product.id})
        self.assertEqual(self.client.delete(f'/core/wishlist/{self.product.id}/').status_code, 204)
        self.assertEqual(self.client.get('/core/wishlist/ids/').json(), [])

    def test_customers_only_and_private(self):
        self.assertIn(self.client.get('/core/wishlist/').status_code, (401, 403))
        self.client.force_authenticate(self.sell.user)
        self.assertEqual(self.client.get('/core/wishlist/').status_code, 403)
        self.client.force_authenticate(self.cust.user)
        self.client.post('/core/wishlist/', {'product': self.product.id})
        other = make_customer('Oth', 'Er')
        self.client.force_authenticate(other.user)
        self.assertEqual(self.client.get('/core/wishlist/ids/').json(), [])
