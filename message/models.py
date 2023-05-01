from django.db import models
from user.models import Profile
import uuid

# Create your models here.
class Message(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    sender = models.ForeignKey(Profile, models.CASCADE, related_name="sent_by")
    receiver = models.ForeignKey(
        Profile, models.CASCADE, related_name="sent_to")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    attachments = models.FileField(upload_to='message_attachments/', null=True)

    def __str__(self):
        return f"message : {self.message} | sent by: {self.sender.user.first_name}, sent_to: {self.receiver.user.first_name}"
