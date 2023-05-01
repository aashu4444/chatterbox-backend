# Generated by Django 4.1.7 on 2023-04-08 07:38

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0004_message_attachments'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='attachments_upload',
            field=models.FileField(null=True, upload_to='message_attachments/'),
        ),
        migrations.AlterField(
            model_name='message',
            name='attachments',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('all', 'All files'), ('pdf', 'PDF'), ('doc', 'DOC'), ('txt', 'TXT')], default='null', max_length=20),
            preserve_default=False,
        ),
    ]