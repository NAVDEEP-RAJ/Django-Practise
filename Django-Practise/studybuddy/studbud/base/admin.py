from django.contrib import admin


from .models import Rooms,topic,Message

admin.site.register(Rooms)
admin.site.register(Topic)
admin.site.register(Message)
# Register your models here.
