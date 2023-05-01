
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.get_chat_messages, name="Get chat messages"),
]
