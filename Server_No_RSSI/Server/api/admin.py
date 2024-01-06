from django.contrib import admin

# Register your models here.

from .models import Note,Location_Schema,Device,Device_Info,RSSI_Info

admin.site.register(Note)
admin.site.register(Device)
admin.site.register(Location_Schema)
admin.site.register(Device_Info)
admin.site.register(RSSI_Info)



