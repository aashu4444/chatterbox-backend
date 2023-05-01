from django.db import models
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django.core import serializers
from django.utils import timezone

# Create your models here.
class AnonymousChatRoom(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
    users = models.JSONField(default=list)

    def time_since_created(self):
        return self._time_since(self.created_on)

    def _time_since(self, datetime_field):
        now = timezone.now()
        delta = now - datetime_field
        seconds = delta.total_seconds()

        if seconds < 60:
            return f'Created {int(seconds)} second{"s" if seconds > 1 else ""} ago'
        elif seconds < 60 * 60:
            minutes = int(seconds / 60)
            return f'Created {minutes} minute{"s" if minutes > 1 else ""} ago'
        elif seconds < 60 * 60 * 24:
            hours = int(seconds / (60 * 60))
            return f'Created {hours} hour{"s" if hours > 1 else ""} ago'
        elif seconds < 60 * 60 * 24 * 30:
            days = int(seconds / (60 * 60 * 24))
            return f'Created {days} day{"s" if days > 1 else ""} ago'
        elif seconds < 60 * 60 * 24 * 365:
            months = int(seconds / (60 * 60 * 24 * 30))
            return f'Created {months} month{"s" if months > 1 else ""} ago'
        else:
            years = int(seconds / (60 * 60 * 24 * 365))
            return f'Created {years} year{"s" if years > 1 else ""} ago'

    def add_user(self, username, isAdmin):
        if not username in self.users:
            self.users.append({'username': username, 'admin': isAdmin})
            self.save()

    def __str__(self):
        return self.name




class AnonymousMessage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    room_id = models.CharField(max_length=200)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    attachments = models.FileField(upload_to='message_attachments/', null=True)
    senderIp = models.CharField(max_length=100)
    user = models.JSONField(default=dict)


    def __str__(self):
        return f"message : {self.message}"


@receiver(post_save, sender=AnonymousMessage)
def my_model_saved(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        message = json.loads(serializers.serialize('json', [instance]))[0]
        room_name = AnonymousChatRoom.objects.get(id=instance.room_id).name

        print(message)
        print(room_name)
        async_to_sync(channel_layer.group_send)(room_name, {'type': "chat_message", "message" : message})
