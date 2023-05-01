# Generated by Django 4.1.5 on 2023-03-28 20:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_profile_connected_profiles'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]