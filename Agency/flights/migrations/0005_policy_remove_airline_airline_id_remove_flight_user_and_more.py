# Generated by Django 5.0.3 on 2024-03-14 12:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0004_airline_flight_airline'),
    ]

    operations = [
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy_id', models.IntegerField(default=0)),
                ('refundable', models.BooleanField(default=False)),
                ('exchangeable', models.BooleanField(default=False)),
                ('exchangeable_condition', models.CharField(blank=True, max_length=255, null=True)),
                ('cancellation_period', models.DurationField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='airline',
            name='airline_id',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='user',
        ),
        migrations.AddField(
            model_name='airline',
            name='policy_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='flights.policy'),
        ),
    ]
