# Generated by Django 5.0.3 on 2024-03-31 19:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_passenger_user_alter_passenger_booking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passenger',
            name='booking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companions', to='booking.booking'),
        ),
    ]
