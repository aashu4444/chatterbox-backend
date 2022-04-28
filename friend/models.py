from django.db import models
from main_user.models import Main_user

class Friend(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Main_user, on_delete=models.CASCADE)
    friends = models.JSONField()

    def __str__(self):
        return f"{self.user.user.first_name}'s friends"
