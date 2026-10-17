from django.db import migrations, models
import django.db.models.deletion


def opening_entries(apps, schema_editor):
    # Keep ledger and balance consistent for sellers who already have a balance.
    seller = apps.get_model('users', 'seller')
    LedgerEntry = apps.get_model('core', 'LedgerEntry')
    for s in seller.objects.exclude(balance=0):
        LedgerEntry.objects.create(seller=s, kind='adjustment', amount=s.balance)


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_email_verified'),
        ('core', '0014_category_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('cod', 'cash on delivery')], default='cod', max_length=3),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('unpaid', 'unpaid'), ('paid', 'paid')], default='unpaid', max_length=6),
        ),
        migrations.CreateModel(
            name='Payout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('paid', 'paid')], default='pending', max_length=7)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('paid_at', models.DateTimeField(blank=True, null=True)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payouts', to='users.seller')),
            ],
            options={'ordering': ['-created', '-id']},
        ),
        migrations.CreateModel(
            name='LedgerEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(choices=[('sale', 'sale'), ('commission', 'commission'), ('payout', 'payout'), ('adjustment', 'adjustment')], max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ledger_entries', to='core.order')),
                ('payout', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ledger_entries', to='core.payout')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ledger', to='users.seller')),
            ],
            options={'ordering': ['-created', '-id']},
        ),
        migrations.RunPython(opening_entries, migrations.RunPython.noop),
    ]
