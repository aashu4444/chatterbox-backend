# Generated by Django 4.1.5 on 2023-04-01 18:01

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_rename_reciever_connectionrequest_receiver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connectionrequest',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
