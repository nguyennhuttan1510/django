from django.contrib import admin

from metadata.models import Metadata


# Register your models here.
class MetadataAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'code', 'type', 'created')


admin.site.register(Metadata, MetadataAdmin)
