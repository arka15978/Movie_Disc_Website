from django.contrib import admin

# Register your models here.

from .models import Room, Movie, Message, User

admin.site.register(User)
admin.site.register(Room)
admin.site.register(Movie)
admin.site.register(Message)
