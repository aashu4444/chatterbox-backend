# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwayI6MTMsImZpZWxkcyI6eyJmaXJzdF9uYW1lIjoiSm9obiIsImxhc3RfbmFtZSI6IkRvZSIsImVtYWlsIjoiZG9lam9obkBnbWFpbC5jb20ifX0.hBL15bpDn5SNyOg5HfnTNeV1JqvZZowqJZI08DWJU4I

from functools import wraps
import jwt, json
from chatterboxBackend.settings import SECRET_KEY
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.core import serializers

def jwt_auth_required(func):

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            # If there is a header named 'auth_token' :
            if not request.headers.get("auth-token") == None:
                auth_token = request.headers.get('auth-token')

                try:
                    decoded_data = jwt.decode(auth_token, SECRET_KEY, algorithms=['HS256'])
                
                except Exception as e:
                    return HttpResponse(status=500, content="Decode error: Inavlid Auth Token.")

                return func(request, decoded_data, *args, **kwargs)
            
            # If there is no header named 'auth_token'
            else:
                print(request.headers.get('auth-token'))
                return HttpResponse(status=401, content="Unauthorized Access!")

        except Exception as e:
            print("error is : ", e)


    return wrapper

def serialize_users(users: list):
    # Convert the user model to json
    serialized_users = json.loads(serializers.serialize('json', users, fields = ('email', 'first_name', 'last_name')))
    print(serialized_users)
    main = []

    # Delete model field from serialized user
    for user in serialized_users:
        main_user = user.copy()
        del main_user["model"]

        main.append(main_user)


    return serialized_users

def serialize_profiles(profiles: list):
    # Convert the user model to json
    serialized_profiles = [profile.to_json() for profile in profiles]
    print(serialized_profiles)
    return serialized_profiles

def del_dict_field(dict_obj, field_name):
    dict_obj_temp = dict_obj.copy()
    del dict_obj_temp[field_name]

    return dict_obj_temp



def sort_ls_for_dict_values(ls, cursor, depth=0):
    keys = [(cursor(item), index) for index, item in enumerate(ls)]
    keys.sort()
    
    sorted_ls = [ls[item[1]] for item in keys]

    return sorted_ls
