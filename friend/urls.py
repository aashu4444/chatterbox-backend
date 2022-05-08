
from . import views
from django.urls import path

urlpatterns = [
    path('getFriends/', views.getFriends),
]