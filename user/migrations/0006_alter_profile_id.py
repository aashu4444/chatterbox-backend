# Generated by Django 4.1.5 on 2023-03-28 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_profile_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.UUIDField(default='<function uuid4 at 0x00000246DC0B8040>', editable=False, primary_key=True, serialize=False),
        ),
    ]
