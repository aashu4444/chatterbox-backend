
from django.urls import path, include
from . import views

urlpatterns = [
    path('room', views.Room.as_view(), name="Room"),
    path('room_names', views.get_room_names, name="Get a list of room names"),
    path('messages', views.get_messages, name="Get messages of a room"),
    path('upload_attachments', views.upload_attachments, name="Upload attachments"),
]
