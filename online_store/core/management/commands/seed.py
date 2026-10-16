import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import product
from users.models import User, seller

CATEGORIES = {
    'Phone': (200, 1500, ['Pro', 'Lite', 'Max', 'Mini', 'Ultra']),
    'Laptop': (400, 2500, ['Air', 'Pro', 'Gaming', 'Slim', 'Book']),
    'Headphones': (20, 350, ['Bass', 'Studio', 'Sport', 'Air', 'Pro']),
    'Watch': (30, 600, ['Fit', 'Classic', 'Sport', 'Smart', 'Lux']),
    'Backpack': (15, 120, ['Urban', 'Trek', 'Daily', 'Travel', 'Mini']),
    'Sneakers': (40, 220, ['Run', 'Street', 'Court', 'Trail', 'Retro']),
    'T-Shirt': (8, 45, ['Basic', 'Graphic', 'Polo', 'Slim', 'Oversize']),
    'Mug': (5, 25, ['Ceramic', 'Travel', 'Magic', 'Steel', 'Classic']),
    'Desk Lamp': (12, 90, ['LED', 'Arc', 'Touch', 'Mini', 'Retro']),
    'Keyboard': (20, 180, ['Mech', 'Wireless', 'RGB', 'Slim', 'Compact']),
}
BRANDS = ['Nova', 'Zeta', 'Orbit', 'Apex', 'Luma', 'Vibe', 'Kora', 'Titan']


class Command(BaseCommand):
    help = 'Seed sellers and products'

    def add_arguments(self, parser):
        parser.add_argument('--products', type=int, default=100)
        parser.add_argument('--sellers', type=int, default=5)

    @transaction.atomic
    def handle(self, *args, **opts):
        random.seed(42)
        sellers = []
        for i in range(1, opts['sellers'] + 1):
            user, created = User.objects.get_or_create(
                username=f'seed_seller{i}',
                defaults={'email': f'seed_seller{i}@example.com',
                          'first_name': 'Seller', 'last_name': str(i)})
            if created:
                user.set_password('seedpass123')
                user.save()
            s, _ = seller.objects.get_or_create(
                user=user,
                defaults={'store_name': f'Store {i}', 'phone_number': f'0910000{i:04d}'})
            sellers.append(s)

        cats = list(CATEGORIES.items())
        items = []
        for n in range(opts['products']):
            cat, (lo, hi, variants) = cats[n % len(cats)]
            brand = random.choice(BRANDS)
            name = f'{brand} {cat} {random.choice(variants)}'[:20]
            price = Decimal(random.uniform(lo, hi)).quantize(Decimal('0.01'))
            items.append(product(
                name=name,
                description=f'{brand} {cat.lower()}, quality item. Fast shipping, 1 year warranty.',
                price=price,
                seller=random.choice(sellers),
                inventory=random.randint(0, 200)))
        product.objects.bulk_create(items)
        self.stdout.write(self.style.SUCCESS(f'Created {len(items)} products, {len(sellers)} sellers'))
