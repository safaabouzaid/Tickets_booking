# Generated by Django 5.0.3 on 2024-03-06 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='flight_id',
            field=models.IntegerField(),
        ),
    ]
