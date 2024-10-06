from django.contrib import admin

from service.models import Service


# Register your models here.

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'capacity', 'price', 'type', 'status', 'organization', 'rate', 'created_by']


admin.site.register(Service, ServiceAdmin)
