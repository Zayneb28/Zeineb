from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_add_email_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='payment_status',
            field=models.BooleanField(default=False),
        ),
    ]
