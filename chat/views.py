from django.shortcuts import HttpResponse
from django.http import JsonResponse
from utils import jwt_auth_required, sort_ls_for_dict_values
from message.models import Message
from django.db.models import Q
from django.core import serializers
import json

@jwt_auth_required
def get_chat_messages(request, decoded_data):
    if request.method == 'GET':
        # Chat user is a user who is chatting with the current logged in user.
        chat_user_id = request.GET['chatUserId']

        # If the chat user is connected with the logged in user
        # if chat_user_id in decoded_data['connected_profiles']:
        chat_messages = Message.objects.filter(
            Q(sender__id=chat_user_id) | Q(receiver__id=chat_user_id),
            Q(sender__id=decoded_data['id']) | Q(receiver__id=decoded_data['id'])
        ).order_by('timestamp')

        # # Decrypt each chat message
        # chat_messages = map(lambda msg:msg.clean(), chat_messages)

        serialized_chat_messages = json.loads(serializers.serialize('json', chat_messages))
        


        return JsonResponse(serialized_chat_messages, safe=False)

        # else:
            # return HttpResponse(status=403, content="Permission not allowed")

