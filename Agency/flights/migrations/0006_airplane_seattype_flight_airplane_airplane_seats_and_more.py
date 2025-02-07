# Generated by Django 5.0.3 on 2024-04-03 19:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0005_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Airplane',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('airplane_name', models.CharField(max_length=100)),
                ('manufacturer', models.CharField(max_length=100)),
                ('manufacturing_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='SeatType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('economy', models.IntegerField(max_length=50, null=True, unique=True)),
                ('business_class', models.IntegerField(max_length=50, null=True, unique=True)),
                ('first_class', models.IntegerField(max_length=50, null=True, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='flight',
            name='airplane',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='flights.airplane'),
        ),
        migrations.AddField(
            model_name='airplane',
            name='seats',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flights.seattype'),
        ),
        migrations.DeleteModel(
            name='FlightSeatClass',
        ),
    ]
