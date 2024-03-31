# Generated by Django 5.0.3 on 2024-03-31 18:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_alter_companion_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('Mr', 'Mr'), ('Ms', 'Ms'), ('Mrs', 'Mrs')], max_length=3)),
                ('passport_number', models.CharField(max_length=20)),
                ('phone_number', models.CharField(blank=True, max_length=100, null=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companions', to='booking.booking')),
            ],
        ),
        migrations.DeleteModel(
            name='Companion',
        ),
    ]
