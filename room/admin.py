from django.contrib import admin

from room.models import Room


# Register your models here.

class RoomAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Room._meta.get_fields() if not field.many_to_many and field.name != 'evaluations']


admin.site.register(Room, RoomAdmin)
