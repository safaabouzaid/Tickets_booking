# Generated by Django 5.0.3 on 2024-04-07 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0007_remove_policy_policy_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='policy',
            name='policy_id',
            field=models.IntegerField(default=1),
        ),
    ]
