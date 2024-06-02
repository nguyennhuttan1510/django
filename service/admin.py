from django.contrib import admin

from service.models import Service


# Register your models here.

class ServiceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Service._meta.get_fields() if not field.many_to_many and field.name != 'evaluation' and field.name !='assetmodel']


admin.site.register(Service, ServiceAdmin)
