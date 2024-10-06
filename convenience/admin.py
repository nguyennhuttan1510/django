from django.contrib import admin

from convenience.models import Convenience


# Register your models here.

class ConvenienceAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'code', 'is_active', 'type', 'priority', 'created_at']


admin.site.register(Convenience, ConvenienceAdmin)
