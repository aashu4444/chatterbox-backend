# Generated by Django 4.1.7 on 2023-04-16 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anonymouschat', '0005_anonymouschatroom_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='anonymousmessage',
            name='user',
            field=models.JSONField(default=dict),
        ),
    ]