from email import message
from django.db import models
from django.dispatch import receiver
from main_user.models import Main_user

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(Main_user, related_name="message_sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(Main_user, related_name="message_reciever", on_delete=models.CASCADE)
    message = models.TextField()
    attachments = models.FileField(upload_to="message")

    def __str__(self) -> str:
        return f"{self.sender.user.first_name} sent : {self.message}"