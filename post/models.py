from django.db import models
from django.contrib.auth.models import User
from main_user.models import Main_user

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Main_user, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    attachments = models.FileField(upload_to="post/post_images", blank=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    user = models.ForeignKey(Main_user, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.comment
