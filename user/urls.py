
from django.urls import path, include
from user import views
from utils import jwt_auth_required
urlpatterns = [
    path('create', views.create),
    path('', views.get_user),
    path('login', views.login),
    path('status', views.get_status),
    path('validate', views.validate),
    path('filter', views.filter),
    path('connection_request', views.ConnectionRequestView.as_view()),
    path('get_connected_profiles', views.get_connected_profiles),
]
