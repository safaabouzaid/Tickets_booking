# Generated by Django 5.0.3 on 2024-03-14 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0008_alter_airline_policy_id_alter_policy_policy_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='airline',
            name='airline_id',
            field=models.IntegerField(default=0),
        ),
    ]
