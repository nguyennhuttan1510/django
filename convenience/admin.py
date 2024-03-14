from django.contrib import admin

from convenience.models import Convenience


# Register your models here.

class ConvenienceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Convenience._meta.get_fields() if not field.many_to_many]


admin.site.register(Convenience, ConvenienceAdmin)
