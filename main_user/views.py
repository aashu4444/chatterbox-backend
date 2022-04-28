from django.http import JsonResponse
from django.shortcuts import HttpResponse
from pip import main
from main_user.forms import SignupForm
from main_user.models import Main_user
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core import serializers
import jwt, json
from django.conf import settings
from django.db.models import Q
from utils import get_user_data

def get_by_auth_token(request):
    try:
        auth_token = request.GET["auth_token"]

        user_data = get_user_data(auth_token)

        return JsonResponse(user_data)

    except Exception as e:
        return HttpResponse("Internal server error!", status=500)


@csrf_exempt
def create_user(request):
    try:
        if request.method == "POST":
            form = SignupForm(request.POST)

            if form.is_valid():
                first_name = request.POST["first_name"]
                username = request.POST["username"]
                last_name = request.POST["last_name"]
                email = request.POST["email"]
                phone = request.POST["phone"]
                password = request.POST["password"]
                profile_image = request.FILES["profile_image"]

                user = User.objects.create_user(username, email, password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                
                main_user = Main_user(user=user, phone=phone, profile_image=profile_image)
                main_user.save()
                return HttpResponse("User successfully created")
            else:
                return HttpResponse(json.dumps(form.errors), status=500)

    except Exception as e:
        print(e)
        return HttpResponse("Internal server error!", status=500)


@csrf_exempt
def login_user(request):
    try:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]

            # Check the credentials are valid or not
            user = authenticate(username=username, password=password)

            if user is not None:
                # If the credentials are valid
                main_user = Main_user.objects.get(user=user)
                user_data = json.loads(serializers.serialize("json", [main_user, user]))

                # Encode the user_data to create a auth token
                encoded_user_data = jwt.encode({"user_data":user_data}, settings.SECRET_KEY, algorithm="HS256")

                return HttpResponse(encoded_user_data)
            
            else:
                # If the credentials are inavalid
                return HttpResponse("Invalid", status=401)

    except Exception as e:
        print(e)
        return HttpResponse("Internal server error!", status=500)


@csrf_exempt
def search_user(request):
    try:
        if request.method == "GET":
            query = request.GET["query"]

            main_user = Main_user.objects.filter(Q(user__first_name__iexact=query) | Q(user__last_name__iexact=query) | Q(user__email__iexact=query))
            
            return JsonResponse(json.loads(serializers.serialize("json", main_user, use_natural_foreign_keys=True, use_natural_primary_keys=True)), safe=False)

    except Exception as e:
        print(e)
        return HttpResponse("Internal server error!", status=500)
