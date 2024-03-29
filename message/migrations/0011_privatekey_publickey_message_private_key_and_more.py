# Generated by Django 4.1.7 on 2023-04-14 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0010_message_encrypted_key_message_iv'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.BinaryField()),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PublicKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.BinaryField()),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='private_key',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='message.privatekey'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='public_key',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='message.publickey'),
            preserve_default=False,
        ),
    ]
