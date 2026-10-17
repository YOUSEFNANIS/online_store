from django.db import migrations, models
import django.db.models.deletion


def completed_to_delivered(apps, schema_editor):
    apps.get_model('core', 'order').objects.filter(order_status='completed').update(order_status='delivered')


def delivered_to_completed(apps, schema_editor):
    apps.get_model('core', 'order').objects.filter(order_status='delivered').update(order_status='completed')


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_product_price'),
    ]

    operations = [
        migrations.RunPython(completed_to_delivered, delivered_to_completed),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(
                choices=[('pending', 'pending'), ('confirmed', 'confirmed'), ('shipped', 'shipped'),
                         ('delivered', 'delivered'), ('cancelled', 'cancelled')],
                default='pending', max_length=9),
        ),
        migrations.CreateModel(
            name='OrderStatusEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=9)),
                ('actor_role', models.CharField(max_length=8)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='core.order')),
            ],
            options={'ordering': ['created', 'id']},
        ),
    ]
