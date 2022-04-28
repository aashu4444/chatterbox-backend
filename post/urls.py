from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create/', views.create_post),
    path('delete/', views.delete_post),
]
