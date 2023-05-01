from django.shortcuts import render, HttpResponse
from .models import Message
from asgiref.sync import async_to_sync
from message.consumers import ChatConsumer
from channels.layers import get_channel_layer
from django.core.files.storage import FileSystemStorage
import json
from django.http import JsonResponse


channel_layer = get_channel_layer()

def room(request, room_name):
    return HttpResponse("")

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
        
        message = Message.objects.get(id=message_id)
        message.attachments = serialized_filenames

        message.save()

        
        return JsonResponse(serialized_filenames, safe=False)