from django.contrib import admin

from django.contrib import admin

from asset.models import AssetModel
from convenience.models import Convenience


# Register your models here.

class AssetAdmin(admin.ModelAdmin):
    list_display = ['asset', 'type', 'created_at']


admin.site.register(AssetModel, AssetAdmin)
