from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

def natual_key(self):
    return {'first_name':self.first_name,'last_name':self.last_name, 'email': self.email}

User.natural_key = natual_key

# Create your models here.
class Main_user(models.Model):
    def delete_user(self):
        pass
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to="profile_images")

    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    