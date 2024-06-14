from django.contrib import admin

from location.models import Location, Country, Province, District, Ward, AdministrativeRegion, AdministrativeUnit


# Register your models here.
class AdministrativeRegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_en', 'code_name', 'code_name_en')


class AdministrativeUnitAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'full_name_en', 'short_name', 'short_name_en', 'code_name', 'code_name_en')


class LocationAdmin(admin.ModelAdmin):
    list_display = ('address', 'province', 'district', 'ward', 'latitude', 'longitude')
    list_select_related = ['province', 'district', 'ward']


class CountryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'country_name', 'code')


class ProvinceAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'name', 'name_en', 'full_name', 'full_name_en', 'code_name', 'administrative_unit',
        'administrative_region')


class DistrictAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'name', 'name_en', 'full_name', 'full_name_en', 'code_name', 'province_code', 'administrative_unit')


class WardAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'name', 'name_en', 'full_name', 'full_name_en', 'code_name', 'district_code', 'administrative_unit')


admin.site.register(AdministrativeRegion, AdministrativeRegionAdmin)
admin.site.register(AdministrativeUnit, AdministrativeUnitAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Ward, WardAdmin)
