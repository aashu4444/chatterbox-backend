from django.db import models
from main_user.models import Main_user

class Friend(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Main_user, on_delete=models.CASCADE)
    friend = models.ForeignKey(Main_user,related_name="given_user_s_friend", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.user.first_name}'s friends"
