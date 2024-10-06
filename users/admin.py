from django.contrib import admin

# Register your models here.
from users.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'middle_name', 'last_name', 'display_name', 'birthday', 'address', 'phone_number', 'email', 'sex', 'national_id', 'owner', 'creator']


admin.site.register(Profile, ProfileAdmin)
