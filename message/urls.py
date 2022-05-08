from nturl2path import url2pathname
from django.urls import path
from message import views

urlpatterns = [
    path('send', views.sendMessage)
]