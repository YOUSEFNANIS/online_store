from django.core.management.base import BaseCommand

from core.models import Category

STARTER_CATEGORIES = [
    ('electronics', 'Electronics', 'إلكترونيات'),
    ('fashion', 'Fashion', 'أزياء'),
    ('home-garden', 'Home & Garden', 'المنزل والحديقة'),
    ('beauty', 'Beauty & Health', 'الجمال والصحة'),
    ('sports', 'Sports & Outdoors', 'الرياضة والهواء الطلق'),
    ('toys', 'Toys & Kids', 'الألعاب والأطفال'),
    ('food', 'Food & Groceries', 'الأغذية والبقالة'),
    ('books', 'Books & Stationery', 'الكتب والقرطاسية'),
    ('automotive', 'Automotive', 'السيارات'),
    ('other', 'Other', 'أخرى'),
]


class Command(BaseCommand):
    help = 'Create the starter product categories (safe to run more than once).'

    def handle(self, *args, **options):
        created = 0
        for slug, name_en, name_ar in STARTER_CATEGORIES:
            _, was_created = Category.objects.get_or_create(slug=slug, defaults={'name_en': name_en, 'name_ar': name_ar})
            created += was_created
        self.stdout.write(self.style.SUCCESS(f'{created} categor{"y" if created == 1 else "ies"} created.'))
