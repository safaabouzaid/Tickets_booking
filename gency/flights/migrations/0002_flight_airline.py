# Generated by Django 5.0.3 on 2024-03-29 20:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='airline',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='flights.airline'),
        ),
    ]
