from django.contrib import admin

# Register your models here.
from users.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'age', 'address', 'phone_number', 'owner', 'creator']


admin.site.register(Profile, ProfileAdmin)
