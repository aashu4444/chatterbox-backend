from django.db import models
from django.dispatch import receiver

from main_user.models import Main_user


class Invite(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(
        Main_user, related_name="invite_sender", on_delete=models.CASCADE)
    reciever = models.ForeignKey(
        Main_user, related_name="invite_reciever", on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)

    

    def __str__(self) -> str:
        return f"{self.sender.user.first_name} sent a invite to : {self.reciever.user.first_name}"
