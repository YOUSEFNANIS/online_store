import random
import urllib.request
from decimal import Decimal
from http.client import HTTPException

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Category, Review, product, productImage
from users.models import User, customer, seller

# slug -> (name_en, name_ar). Existing categories (see seed_categories) are reused by slug.
CATEGORIES = {
    'electronics': ('Electronics', 'إلكترونيات'),
    'fashion': ('Fashion', 'أزياء'),
    'home-kitchen': ('Home & Kitchen', 'المنزل والمطبخ'),
    'beauty': ('Beauty', 'الجمال'),
    'sports': ('Sports', 'الرياضة'),
    'toys': ('Toys & Kids', 'الألعاب والأطفال'),
    'books': ('Books', 'الكتب'),
    'food': ('Grocery', 'البقالة'),
}

# username, store_name (max 20), phone (max 11)
SELLERS = [
    ('nova_tech', 'Nova Tech', '01000000001'),
    ('urban_thread', 'Urban Thread', '01000000002'),
    ('casa_verde', 'Casa Verde', '01000000003'),
    ('glow_lab', 'Glow Lab', '01000000004'),
    ('peak_sports', 'Peak Sports', '01000000005'),
    ('little_joy', 'Little Joy', '01000000006'),
    ('page_turner', 'Page Turner', '01000000007'),
    ('fresh_basket', 'Fresh Basket', '01000000008'),
    ('sound_hub', 'Sound Hub', '01000000009'),
    ('pixel_gear', 'Pixel Gear', '01000000010'),
    ('atelier_9', 'Atelier 9', '01000000011'),
    ('nest_co', 'Nest & Co', '01000000012'),
]

# name (max 20), store, category slug, price, rating, description
PRODUCTS = [
    ('ANC Headphones', 'Nova Tech', 'electronics', '89.00', 4.8, 'Wireless noise-cancelling headphones.'),
    ('4K Action Camera', 'Nova Tech', 'electronics', '129.00', 4.6, '4K action camera with waterproof case.'),
    ('Bluetooth Speaker', 'Sound Hub', 'electronics', '34.90', 4.7, 'Portable Bluetooth speaker.'),
    ('RGB Gaming Keyboard', 'Pixel Gear', 'electronics', '59.00', 4.5, 'Mechanical gaming keyboard with RGB lighting.'),
    ('Power Bank 20000mAh', 'Sound Hub', 'electronics', '27.50', 4.8, 'Fast charging power bank, 20,000mAh.'),
    ('Linen Summer Shirt', 'Urban Thread', 'fashion', '32.00', 4.7, 'Linen summer shirt, relaxed fit.'),
    ('Classic Denim Jacket', 'Urban Thread', 'fashion', '68.00', 4.6, 'Classic denim jacket.'),
    ('Leather Crossbody', 'Atelier 9', 'fashion', '74.00', 4.8, 'Minimal leather crossbody bag.'),
    ('White Sneakers', 'Peak Sports', 'fashion', '49.00', 4.7, 'Everyday white sneakers.'),
    ('Merino Wool Scarf', 'Atelier 9', 'fashion', '26.00', 4.9, 'Soft merino wool scarf.'),
    ('Cast Iron Skillet', 'Casa Verde', 'home-kitchen', '38.00', 4.9, 'Cast iron skillet, 26cm.'),
    ('Pour-Over Coffee Set', 'Casa Verde', 'home-kitchen', '29.00', 4.7, 'Ceramic pour-over coffee set.'),
    ('Bamboo Organizer Set', 'Nest & Co', 'home-kitchen', '21.50', 4.5, 'Bamboo storage organizer set.'),
    ('Steel Water Bottle', 'Nest & Co', 'home-kitchen', '18.00', 4.8, 'Stainless steel water bottle, 1L.'),
    ('Cotton Bedding Set', 'Casa Verde', 'home-kitchen', '79.00', 4.6, 'Soft cotton bedding set, queen size.'),
]

REVIEWERS = ['demo_buyer1', 'demo_buyer2', 'demo_buyer3', 'demo_buyer4']
PASSWORD = 'demopass123'


class Command(BaseCommand):
    help = 'Seed the demo marketplace data shown on the landing page (safe to run more than once).'

    def add_arguments(self, parser):
        parser.add_argument('--images', action='store_true',
                            help='Download a placeholder picture per product from picsum.photos (needs internet).')

    @transaction.atomic
    def handle(self, *args, **opts):
        random.seed(7)

        cats = {}
        for slug, (en, ar) in CATEGORIES.items():
            cats[slug], _ = Category.objects.get_or_create(slug=slug, defaults={'name_en': en, 'name_ar': ar})

        sellers = {}
        for username, store, phone in SELLERS:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': f'{username}@example.com', 'first_name': store, 'last_name': 'Store', 'email_verified': True})
            if created:
                user.set_password(PASSWORD)
                user.save()
            sellers[store], _ = seller.objects.get_or_create(user=user, defaults={'store_name': store, 'phone_number': phone})

        buyers = []
        for i, username in enumerate(REVIEWERS, 1):
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': f'{username}@example.com', 'first_name': 'Buyer', 'last_name': str(i), 'email_verified': True})
            if created:
                user.set_password(PASSWORD)
                user.save()
            c, _ = customer.objects.get_or_create(user=user, defaults={'phone_number': f'0111000000{i}'})
            buyers.append(c)

        made = 0
        for name, store, slug, price, rating, desc in PRODUCTS:
            assert len(name) <= 20, name
            p, created = product.objects.get_or_create(
                name=name, seller=sellers[store],
                defaults={'description': desc, 'price': Decimal(price), 'inventory': random.randint(20, 200), 'category': cats[slug]})
            made += created
            for b in buyers:
                # Spread ratings around the landing-page average, clamped to 1..5.
                stars = max(1, min(5, round(rating + random.choice([-1, 0, 0, 0, 1]))))
                Review.objects.get_or_create(product=p, customer=b, defaults={'rating': stars, 'text': 'Great value, arrived fast.'})
            if opts['images'] and not p.images.exists():
                self.add_image(p)

        self.stdout.write(self.style.SUCCESS(
            f'{made} products created ({len(PRODUCTS) - made} already existed), {len(SELLERS)} stores, {len(buyers)} buyers. '
            f'Demo login password: {PASSWORD}'))

    def add_image(self, p):
        url = f'https://picsum.photos/seed/p{p.pk}/600/600'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        data = None
        for _ in range(3):
            try:
                with urllib.request.urlopen(req, timeout=20) as r:
                    data = r.read()
                break
            except (OSError, HTTPException) as e:  # IncompleteRead is an HTTPException, not an OSError
                err = e
        if data is None:
            self.stderr.write(f'No image for {p.name}: {err!r}')
            return
        img = productImage(product=p)
        img.image.save(f'demo_{p.pk}.jpg', ContentFile(data), save=True)
