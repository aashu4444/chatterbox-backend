
from django.urls import path, include
from user import views

urlpatterns = [
    path('create', views.create),
    path('login', views.login),
    path('validate', views.validate),
    path('filter', views.filter),
    path('connection_request', views.ConnectionRequestView.as_view()),
    path('get_connected_profiles', views.get_connected_profiles),
]
