
import json
from .models import Message
from user.models import Profile
from django.core import serializers
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from anonymouschat.models import AnonymousChatRoom, AnonymousMessage
from datetime import datetime
from django.core.exceptions import ValidationError
# TODO : Write aync websocket consumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Change the disconnected user's status to "Not active" by change the 'status' field to the type of disconnect
        try:
            profile_id = self.room_name.replace("_", '-') # Replace '_' with '-' to convert it into a valid UUID.
            profile = Profile.objects.get(id=profile_id)
            profile.status = json.dumps({'status': f"Last active on {datetime.now()}", 'code': 0})
            profile.save()

            print("Disconnected :", profile.get_status())
        except ValidationError as e:
            
            pass



    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        anonymous = text_data_json.get("anonymous", None)
        message = text_data_json["message"]
        share_status = text_data_json.get('share_status', 0)

        if anonymous == 'true' or anonymous != None:
            senderIp = text_data_json['senderIp']
            username = text_data_json['username']

            user = {
                'username': username,
                'admin': list(filter(lambda user: user['username'] == username, AnonymousChatRoom.objects.get(name=self.room_name).users))[0]['admin']
            }

            message_obj = AnonymousMessage(
                message=message,
                room_id=AnonymousChatRoom.objects.get(name=self.room_name).id,
                senderIp=senderIp,
                user=user
            )
            message_obj.save()

        elif share_status == 1:
            async_to_sync(self.channel_layer.group_send)(self.room_name, {
                'type': "share_status", "status": "Active Now"})

        # If the current user is logged in
        else:
            room_name = text_data_json["room_name"]
            sender_id = text_data_json['sender_id']
            receiver_id = text_data_json['receiver_id']

            message_obj = Message(
                sender=Profile.objects.get(id=sender_id),
                receiver=Profile.objects.get(id=receiver_id),
                message=message
            )

            message_obj.save()

            serialized_msg_obj = json.loads(
                serializers.serialize('json', [message_obj]))[0]

            # Send the message object to the message receiver
            async_to_sync(self.channel_layer.group_send)(
                room_name, {'type': "chat_message", "message": serialized_msg_obj})

            # Send the message object to message sender
            async_to_sync(self.channel_layer.group_send)(sender_id.replace(
                '-', '_'), {'type': "chat_message", "message": serialized_msg_obj})

    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps(
            {"type": "chat_message", "message": message}))

    def share_status(self, event):
        status = event["status"]

        # Send status to WebSocket
        self.send(text_data=json.dumps(
            {"type": "user_status", "status": status}))

    def my_message_type(self, event):
        data = event['data']

        print("Helllo praaaa")
