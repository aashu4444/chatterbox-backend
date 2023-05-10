from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
import uuid
import json

class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.OneToOneField(User, models.CASCADE)
    connected_profiles = models.JSONField(default=list)
    status = models.TextField(max_length=100, default="")

    def get_status(self):
        return json.loads(self.status)

    def connect_profile(self, connect_to_id):
        
        self.connected_profiles_temp = self.connected_profiles.copy()
        self.connected_profiles_temp.append(str(connect_to_id))

        self.connected_profiles = self.connected_profiles_temp
        self.save()

    def to_json(self):
        return dict(
            id=str(self.id),
            first_name=self.user.first_name,
            last_name=self.user.last_name,
            email=self.user.email,
            connected_profiles=self.connected_profiles,
        )

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

@receiver(post_save, sender=Profile)
def profile_change_detector(sender, instance, **kwargs):
    print('Something change here .....')
    print(instance.status)
    
  
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Exception as e:
        pass




class ConnectionRequest(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    sender = models.ForeignKey(Profile, models.CASCADE, related_name='request_sent_by')
    receiver = models.ForeignKey(Profile, models.CASCADE, related_name='request_recieved_by')
    time = models.DateTimeField(auto_now_add=True)

    def to_json(self):
        return dict(
            id=self.id,
            sender = dict(
                id=str(self.sender.id),
                first_name=self.sender.user.first_name,
                last_name=self.sender.user.last_name,
            ),
            receiver = dict(
                id=str(self.receiver.id),
                first_name=self.receiver.user.first_name,
                last_name=self.receiver.user.last_name,
            ),

            time=self.time

        )

    def __str__(self):
        return f"{self.sender.user.first_name} sent a request to : {self.receiver.user.first_name}"
    
