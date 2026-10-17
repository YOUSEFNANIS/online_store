from django.db import migrations, models


def verify_existing_users(apps, schema_editor):
    # Accounts created before verification existed are treated as verified.
    apps.get_model('users', 'User').objects.update(email_verified=True)


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_seller_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(verify_existing_users, migrations.RunPython.noop),
    ]
