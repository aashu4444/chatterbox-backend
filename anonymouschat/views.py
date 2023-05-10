from django.shortcuts import render, HttpResponse, get_object_or_404
import json
from .models import AnonymousChatRoom, AnonymousMessage
from django.core import serializers
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.files.storage import FileSystemStorage
from django.views import View
from django.utils.decorators import method_decorator

class Room(View):

    def post(self, request, *args, **kwargs):
        try:
            params = json.loads(request.body)
            print(params)
            room_name = params['roomName'].lower()
            username = params['username'].lower()
        except KeyError:
            return HttpResponseBadRequest("Invalid request body")

        if AnonymousChatRoom.objects.filter(name=room_name).exists():
            return HttpResponse(status=503, content=f"Room '{room_name}' already exists! Please enter another name.")
        else:
            anonymous_chat_room = AnonymousChatRoom.objects.create(name=room_name)
            anonymous_chat_room.add_user(username, True)
            return HttpResponse(f"Room '{room_name}' created successfully!")

    def put(self, request, *args, **kwargs):
        room_name = request.GET['roomName'].lower()
        username = request.GET['username'].lower()

        anonymous_chat_room = get_object_or_404(AnonymousChatRoom, name=room_name)
        already_added = username.lower() in {user['username'].lower() for user in anonymous_chat_room.users}

        if not already_added:
            anonymous_chat_room.add_user(username, False)


        return HttpResponse(f"Room '{room_name}' exists and can be joined!")

    def get(self, request, *args, **kwargs):
        room_name = request.GET['roomName']

        try:
            anonymous_chat_room = AnonymousChatRoom.objects.values().get(name=room_name)
            return JsonResponse(anonymous_chat_room)
        except AnonymousChatRoom.DoesNotExist:
            return HttpResponse(status=404,content = f"Anonymous ChatRoom '{room_name}' does not exist")

def create_room(request):
    if request.method == 'POST':
        try:
            room_name = request.POST['roomName']
            username = request.GET['username']
        except KeyError:
            return HttpResponseBadRequest("Invalid request body")

        if AnonymousChatRoom.objects.filter(name=room_name).exists():
            return HttpResponse(status=503, content=f"Room '{room_name}' already exists! Please enter another name.")
        else:
            AnonymousChatRoom.objects.create(name=room_name)
            anonymous_chat_room.add_user(username, True)
            return HttpResponse(f"Room '{room_name}' created successfully!")


def join_room(request):
    if request.method == 'GET':
        room_name = request.GET['roomName']
        username = request.GET['username']

        anonymous_chat_room = get_object_or_404(AnonymousChatRoom, name=room_name)
        already_added = username.lower() in {user['username'].lower() for user in anonymous_chat_room.users}

        if not already_added:
            anonymous_chat_room.add_user(username, False)


        return HttpResponse(f"Room '{room_name}' exists and can be joined!")


def get_messages(request):
    if request.method == "GET":
        room_name = request.GET['roomName']

        messages = AnonymousMessage.objects.filter(
            room_id = AnonymousChatRoom.objects.get(name=room_name).id
        )

        serialized_messages = serializers.serialize('json', messages)

        return JsonResponse(serialized_messages, safe=False)


def get_room_names(request):
    if request.method == 'GET':
        query = request.GET.get("query")

        if query:
            room_names = [item for item in AnonymousChatRoom.objects.filter(name__icontains=query).values('name')]

        else:
            room_names = [item for item in AnonymousChatRoom.objects.values_list('name', flat=True)]
        
        return JsonResponse(room_names, safe=False)



def upload_attachments(request):
    if request.method == "POST":
        message_id = request.POST['message_id']
        # Get the uploaded files from request.FILES
        uploaded_files = request.FILES.getlist('attachments')

        print(uploaded_files)
        
        fs = FileSystemStorage()
        
        filenames = []
        
        for f in uploaded_files:
            filename = fs.save(f.name, f)
            filenames.append(filename)
        
        serialized_filenames = json.dumps(filenames)
        
        message = AnonymousMessage.objects.get(id=message_id)
        message.attachments = serialized_filenames

        message.save()

        
        return JsonResponse(serialized_filenames, safe=False)