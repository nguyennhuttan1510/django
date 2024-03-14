from django.contrib import admin

from organization.models import Organization


# Register your models here.
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'zipcode', 'phone', 'rate', 'owner')


admin.site.register(Organization, OrganizationAdmin)
