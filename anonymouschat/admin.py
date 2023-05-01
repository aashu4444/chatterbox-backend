from django.contrib import admin
from .models import AnonymousChatRoom, AnonymousMessage

# Register your models here.
admin.site.register(AnonymousChatRoom)
admin.site.register(AnonymousMessage)