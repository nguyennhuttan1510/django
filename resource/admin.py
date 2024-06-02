from django.contrib import admin

from resource.models import Resource


# Register your models here.
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'file')

admin.site.register(Resource, ResourceAdmin)