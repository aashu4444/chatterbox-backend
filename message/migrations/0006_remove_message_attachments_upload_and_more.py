# Generated by Django 4.1.7 on 2023-04-08 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0005_message_attachments_upload_alter_message_attachments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='attachments_upload',
        ),
        migrations.AlterField(
            model_name='message',
            name='attachments',
            field=models.FileField(null=True, upload_to='message_attachments/'),
        ),
    ]
