from django.shortcuts import HttpResponse
from main_user.models import Main_user
from utils import login_required, get_user_data
from .models import Invite
from django.views.decorators.csrf import csrf_exempt
import json
from friend.models import Friend
from django.core import serializers

@login_required
@csrf_exempt
def send_invite(request, user_data):
    try:
        if request.method == "POST":
            target_user_id = request.POST["target_user_id"]
            print(user_data)

            try:
                sender = Main_user.objects.get(id=user_data["main_user_id"])
                reciever = Main_user.objects.get(id=target_user_id)
            except Invite.DoesNotExist as e:
                return HttpResponse("Sender/Reciever not found!", status=404)

            # Check that the user has aleready sent a invite or not?
            if Invite.objects.filter(sender=sender, reciever=reciever).count() != 0:
                return HttpResponse("Invite aleready exists!", status=500)

            else:
                Invite.objects.create(sender=sender, reciever=reciever)

            return HttpResponse("Invite sent successfully!")
    except Exception as e:
        print(e)
        return HttpResponse("Internal server error!", 500)


@login_required
@csrf_exempt
def cancel_invite(request, user_data):
    try:
        if request.method == "DELETE":
            target_user_id = json.loads(request.body)["target_user_id"]

            try:
                sender = Main_user.objects.get(id=user_data["main_user_id"])
                reciever = Main_user.objects.get(id=target_user_id)
            except Invite.DoesNotExist as e:
                return HttpResponse("Sender/Reciever not found!", status=404)

            invite = Invite.objects.get(sender=sender, reciever=reciever)
            invite.delete()

            return HttpResponse("Invite cancelled successfully!")
    except Exception as e:
        return HttpResponse("Internal server error!", 500)


@login_required
@csrf_exempt
def accept_invite(request, user_data):
    try:
        if request.method == "PUT":
            target_user_id = json.loads(request.body)["target_user_id"]
            loggedin_user = Main_user.objects.get(id=user_data["main_user_id"])

            try:
                sender = Main_user.objects.get(id=target_user_id)
                reciever = loggedin_user
            except Invite.DoesNotExist as e:
                return HttpResponse("Sender/Reciever not found!", status=404)

            invite = Invite.objects.get(sender=sender, reciever=reciever)
            invite.accepted = True
            invite.save()

            friend_obj = Friend.objects.filter(user=loggedin_user)
            if friend_obj.count() == 0:
                Friend.objects.create(user=loggedin_user, friends=[serializers.serialize("json",[reciever])])
            else:
                friend_obj.friends = [user for user in friend_obj.friends].append(reciever)
                friend_obj.save()



            return HttpResponse("Invite accepted successfully!")
    except Exception as e:
        print(e)
        return HttpResponse("Internal server error!", 500)

