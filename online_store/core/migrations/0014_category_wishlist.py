from django.db import migrations, models
import django.db.models.deletion

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


def seed_categories(apps, schema_editor):
    Category = apps.get_model('core', 'Category')
    for slug, name_en, name_ar in STARTER_CATEGORIES:
        Category.objects.get_or_create(slug=slug, defaults={'name_en': name_en, 'name_ar': name_ar})


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_email_verified'),
        ('core', '0013_review_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('name_en', models.CharField(max_length=60)),
                ('name_ar', models.CharField(max_length=60)),
            ],
            options={'verbose_name_plural': 'categories', 'ordering': ['id']},
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='core.category'),
        ),
        migrations.CreateModel(
            name='WishlistItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to='users.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlisted_by', to='core.product')),
            ],
            options={'ordering': ['-created', '-id'], 'unique_together': {('customer', 'product')}},
        ),
        migrations.RunPython(seed_categories, migrations.RunPython.noop),
    ]
