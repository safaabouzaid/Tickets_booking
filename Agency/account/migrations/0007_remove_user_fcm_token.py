# Generated by Django 5.0.3 on 2024-04-12 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_user_fcm_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='fcm_token',
        ),
    ]
