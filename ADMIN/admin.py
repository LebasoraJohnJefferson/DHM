from django.contrib import admin
from .models import Secretary, Event, Comment, Property, Message

# Register your models here.
admin.site.register(Secretary)
admin.site.register(Event)
admin.site.register(Comment)
admin.site.register(Property)
admin.site.register(Message)
