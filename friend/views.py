
from django.shortcuts import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from friend.models import Friend
from django.db.models import Q
from utils import login_required
from main_user.models import Main_user
from django.http import JsonResponse
from django.core import serializers


@csrf_exempt
@login_required
def getFriends(request, user_data):
    try:
        if request.method == 'GET':
            loggedin_user = Main_user.objects.get(id=user_data["main_user_id"])

            def getFriend(friend):
                """This function returns data of the friend only.
                (Not of the loggedin user)"""
                print(friend.user.id==user_data['main_user_id'])
                if friend.user.id==user_data['main_user_id']:
                    return friend.friend
                else:
                    return friend.user
            friends = list(map(getFriend, Friend.objects.filter(Q(user=loggedin_user) | Q(friend=loggedin_user))))

            return JsonResponse(json.loads(serializers.serialize('json', friends, use_natural_foreign_keys=True)), safe=False)

    except Exception as e:
        print(e)
        return HttpResponse("Internal server error!", status=500)