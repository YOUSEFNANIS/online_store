from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0007_user_email_verified'),
        ('core', '0012_order_lifecycle'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])),
                ('text', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='users.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='core.product')),
            ],
            options={'ordering': ['-created', '-id'], 'unique_together': {('product', 'customer')}},
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(choices=[('spam', 'spam'), ('fraud', 'fraud'), ('inappropriate', 'inappropriate'), ('counterfeit', 'counterfeit'), ('other', 'other')], max_length=13)),
                ('details', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('open', 'open'), ('resolved', 'resolved'), ('dismissed', 'dismissed')], default='open', max_length=9)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='core.product')),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to=settings.AUTH_USER_MODEL)),
                ('seller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='users.seller')),
            ],
            options={'ordering': ['-created', '-id']},
        ),
    ]
