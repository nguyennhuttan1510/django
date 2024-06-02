from django.contrib import admin

from location.models import Location, Country, City, District, Ward


# Register your models here.
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'location_name', 'address', 'city', 'district', 'ward', 'latitude', 'longitude')


class CountryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'country_name', 'code')


class CityAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'city_name', 'code', 'postal_code')


class DistrictAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'district_name', 'code')


class WardAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'ward_name', 'code')


admin.site.register(Location, LocationAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Ward, WardAdmin)
