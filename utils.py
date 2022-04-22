from django.http import HttpResponse
import jwt, json
from django.conf import settings
from functools import wraps
from django.http import QueryDict

from django.shortcuts import HttpResponse



def get_user_data(auth_token):
    user_data = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])


    # user_data contains data of two models (main_user, auth.user), merge fields of both models into one.
    fields = {}
    main_user_fields = user_data["user_data"][0]["fields"]
    main_user_fields["main_user_id"] = user_data["user_data"][0]["pk"]

    user_fields = user_data["user_data"][1]["fields"]
    user_fields["user_id"] = user_data["user_data"][1]["pk"]
    
    fields.update(main_user_fields)
    fields.update(user_fields)

    return fields


def login_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        auth_token = request.headers.get("auth-token")
        if auth_token == None:
            return HttpResponse("Unauthorized access!", status=401)
        else:
            user_data = get_user_data(auth_token)

            return view(request, user_data, *args, **kwargs)
    
    return wrapper

def query_data(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        request_data = json.loads(request.body)
        return view(request, request_data, *args, **kwargs)
    
    return wrapper

