# Generated by Django 4.1.5 on 2023-03-28 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_remove_profile_profile_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connectionrequest',
            name='reciever',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_recieved_by', to='user.profile'),
        ),
        migrations.AlterField(
            model_name='connectionrequest',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_sent_by', to='user.profile'),
        ),
    ]
