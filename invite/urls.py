from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('send/', views.send_invite),
    path('cancel/', views.cancel_invite),
    path('accept/', views.accept_invite),
    path('isInvited/', views.isInvited),
]
