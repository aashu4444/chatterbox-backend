from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from .forms import SignupForm, LoginForm
from .models import ConnectionRequest, Profile
from django.contrib.auth import authenticate
from django.core import serializers
import json
import jwt
from chatterboxBackend.secret import SECRET_KEY
from utils import jwt_auth_required, serialize_users, serialize_profiles, del_dict_field
from django.http import JsonResponse
from django.db.models import Q
from django.views import View
from django.utils.decorators import method_decorator


def create(request):
    if request.method == 'POST':

        email = request.POST["email"]
        password = request.POST["password"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        form = SignupForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=email, email=email, first_name=first_name, last_name=last_name, password=password)

            return HttpResponse(f"User created successfully!")

        else:
            return HttpResponse(status=401, content=form.errors.as_json())

    return HttpResponse(request.method)


def login(request):
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST["password"]

        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(username=email, password=password)
            if user is not None:
                profile = Profile.objects.get(user=user)
                serialized_user = profile.to_json();

                # Encode the serialized user to json web token (jwt)
                encoded_jwt = jwt.encode(
                    serialized_user, SECRET_KEY, algorithm="HS256")

                return HttpResponse(encoded_jwt)

            else:
                return HttpResponse(status=401, content="Invalid credentials")

        else:
            return HttpResponse(status=401, content=form.errors.as_json())


class ConnectionRequestView(View):
    @method_decorator(jwt_auth_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, decoded_data, *args, **kwargs):
        """
        Request : Send a connection request to a user.

        Request Type : POST
        URL : /user/connection_request

        Parameters : 
        'receiver_id' => The id of the profile from which the current user wants to connect.
        """
        sender_id = decoded_data['id']
        receiver_id = request.POST['receiver_id']
        
        approved = sender_id!=receiver_id and ConnectionRequest.objects.filter(receiver__id=receiver_id).exists()==False

        if approved:
            sender = Profile.objects.get(id=sender_id)
            receiver = Profile.objects.get(id=receiver_id)

            connection_request = ConnectionRequest.objects.create(
                sender=sender,
                receiver=receiver,
            )

            return JsonResponse(connection_request.to_json(), safe=False)

    def get(self, request, decoded_data, *args, **kwargs):
        """
        Request : Fetch requests of user

        REQUEST TYPE : GET
        URL : /user/connection_request

        PARAMETERS:
        'requests_type' (sent/received) : which type of requests you want to fetch?
        """

        requests_type = request.GET['requests_type']

        if requests_type == 'received':
            # Code for fetching recieved requests :
            connection_requests = ConnectionRequest.objects.filter(
                receiver__id=decoded_data['id'])

        elif requests_type == 'sent':
            # Code for fetching recieved requests :
            connection_requests = ConnectionRequest.objects.filter(
                sender__id=decoded_data['id'])

        return JsonResponse([connection_request.to_json() for connection_request in connection_requests], safe=False)

    def options(self, request, decoded_data, *args, **kwargs):
        """
        Request : Cancel a sent request

        REQUEST TYPE : OPTIONS
        URL : /user/connection_request

        PARAMETERS:
        'request_id' : Id of the request which user wants to delete
        """

        params = json.loads(request.body)
        request_id = params['request_id']

        ConnectionRequest.objects.get(
            id=request_id
        ).delete()


        return HttpResponse("Connection request canceled!")



    def put(self, request, decoded_data, *args, **kwargs):
        params = json.loads(request.body)

        connection_request_id = params['connection_request_id']
        connection_request = ConnectionRequest.objects.get(
            id=connection_request_id)


        if str(connection_request.receiver.id) == decoded_data['id']:
            connection_request.sender.connect_profile(
                connection_request.receiver.id)
            connection_request.receiver.connect_profile(
                connection_request.sender.id)
                
            connection_request.delete()

            return HttpResponse("Connection request accepted!")

        else:
            return HttpResponse(status=403, content="Action not allowed!")

    def delete(self, request, decoded_data, *args, **kwargs):
        params = json.loads(request.body)

        connection_request_id = params['connection_request_id']
        connection_request = ConnectionRequest.objects.get(
            id=connection_request_id)

        if str(connection_request.receiver) == decoded_data['id']:
            connection_request.delete()
            return HttpResponse("Connection request declined!")

        else:
            return HttpResponse(status=403, content="Action not allowed!")



@jwt_auth_required
def validate(request, decoded_data):
    print("It's validating!")
    return JsonResponse(decoded_data)


@jwt_auth_required
def filter(request, decoded_data):
    if request.method == "GET":
        query = request.GET['query']
        print(query)

        found_profiles = Profile.objects.filter(Q(user__first_name__icontains=query) | Q(
            user__last_name__icontains=query) | Q(user__username__icontains=query))

        return HttpResponse(json.dumps(serialize_profiles(found_profiles)))



@jwt_auth_required
def get_connected_profiles(request, decoded_data):
    if request.method == "GET":
        
        # Fetch Profile object of current logged in user
        profile = Profile.objects.get(id=decoded_data['id'])

        # Get the 'connected_profiles' column
        connected_profiles = [
            del_dict_field(Profile.objects.get(id=profile_id).to_json(), 'connected_profiles')

            for profile_id in profile.connected_profiles
        ]

        return JsonResponse(connected_profiles, safe=False)

