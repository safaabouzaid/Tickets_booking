# Generated by Django 5.0.3 on 2024-04-15 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_remove_user_fcm_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='balance',
            field=models.DecimalField(decimal_places=5, max_digits=15, null=True),
        ),
    ]
