from message.models import Message
from utils import login_required
from django.shortcuts import  HttpResponse
from django.views.decorators.csrf import csrf_exempt
from main_user.models import Main_user

@csrf_exempt
@login_required
def sendMessage(request, user_data):
    try:
        if request.method == 'POST':
            target_user_id = request.POST['target_user_id']
            message = request.POST['message']
            loggedin_user = Main_user.objects.get(id=user_data['main_user_id'])
            target_user = Main_user.objects.get(id=target_user_id)

            message = Message(sender=loggedin_user, receiver=target_user, message=message)
            message.save()

            return HttpResponse("Message sent successfully!")


    except Exception as e:
        print(e)
        return HttpResponse("Internal server error!", status=500)