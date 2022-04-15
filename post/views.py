from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from post.models import Post
from main_user.models import Main_user
import json
from django.conf import UserSettingsHolder, settings
from django.views.decorators.http import require_http_methods
from utils import login_required, query_data
from django.http import JsonResponse
from django.core import serializers


@csrf_exempt
@login_required
def create_post(request, user_data):
    try:
        if request.method == "POST":
            text = request.POST.get("text")
            attachments = request.FILES.get("attachments")

            main_user = Main_user.objects.get(id=user_data["main_user_id"])

            post = Post(user=main_user, text=text, attachments=attachments)
            post.save()

            return JsonResponse(json.loads(serializers.serialize("json", [post]))[0], safe=False)

    except Exception as e:
        return HttpResponse("Internal server error!", status=500)


@csrf_exempt
@login_required
@query_data
def delete_post(request, request_data, user_data):
    try:
        if request.method == "DELETE":
            post_id = request_data.get("post_id")

            try:
                post = Post.objects.get(id=post_id)
                post.delete()
                return HttpResponse("Post successfully deleted!")

            except Post.DoesNotExist as error:
                return HttpResponse("Post not found!", status=404)

    except Exception as e:
        return HttpResponse("Internal server error!", status=500)
