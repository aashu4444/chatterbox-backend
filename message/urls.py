
from django.urls import path, include
from . import views

urlpatterns = [
    path('upload_attachments', views.upload_attachments),
    path("<str:room_name>/", views.room, name="room"),
]

