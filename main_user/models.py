import json
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core import serializers


def natual_key(self):
    return {'first_name': self.first_name, 'last_name': self.last_name, 'email': self.email, 'username': self.username, "user_id":self.id}


User.natural_key = natual_key



class Main_user(models.Model):
    def delete_user(self):
        pass
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to="profile_images")

    def stringify(self, dump=True):
        serialized = json.loads(serializers.serialize(
            'json', [self], use_natural_foreign_keys=True))[0]
        serialized.update(
            {key: value for key, value in serialized["fields"].items()})
        serialized.update(
            {key: value for key, value in serialized["user"].items()})

        del serialized["fields"], serialized["user"]

        return json.dumps(serialized) if dump == True else serialized

    def natural_key(self):
        return {
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'email': self.user.email,
                'username': self.user.username,
                'phone': self.phone,
                'main_user_id':self.id,
                'asds':'aa'
        }

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
