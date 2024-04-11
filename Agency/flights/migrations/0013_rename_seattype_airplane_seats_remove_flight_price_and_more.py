# Generated by Django 5.0.3 on 2024-04-11 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0012_rename_airpline_airplane_airline_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='airplane',
            old_name='seattype',
            new_name='seats',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='price',
        ),
        migrations.AddField(
            model_name='flight',
            name='business_remaining',
            field=models.IntegerField(default=10, null=True),
        ),
        migrations.AddField(
            model_name='flight',
            name='economy_remaining',
            field=models.IntegerField(default=20, null=True),
        ),
        migrations.AddField(
            model_name='flight',
            name='first_remaining',
            field=models.IntegerField(default=10, null=True),
        ),
    ]
