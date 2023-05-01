# Generated by Django 4.1.7 on 2023-04-14 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0006_remove_message_attachments_upload_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='encrypted_key',
            field=models.BinaryField(default=b''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='iv',
            field=models.BinaryField(default=b''),
            preserve_default=False,
        ),
    ]