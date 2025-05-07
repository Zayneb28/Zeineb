from django.db import migrations, models

def set_default_email(apps, schema_editor):
    Booking = apps.get_model('bookings', 'Booking')
    for booking in Booking.objects.all():
        if not booking.email:
            booking.email = 'unknown@example.com'
            booking.save()

class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='email',
            field=models.EmailField(default='unknown@example.com', max_length=254),
            preserve_default=False,
        ),
        migrations.RunPython(set_default_email),
    ]
