from django.db import models


# Create your models here.
class AdministrativeRegion(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    name_en = models.CharField(max_length=50)
    code_name = models.CharField(max_length=50)
    code_name_en = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class AdministrativeUnit(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    full_name = models.CharField(max_length=80)
    full_name_en = models.CharField(max_length=80)
    short_name = models.CharField(max_length=50)
    short_name_en = models.CharField(max_length=50)
    code_name = models.CharField(max_length=80)
    code_name_en = models.CharField(max_length=80)

    def __str__(self):
        return f'{self.full_name}'


class Country(models.Model):
    country_name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.country_name}'


class Province(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=50)
    name_en = models.CharField(max_length=50, null=True)
    full_name = models.CharField(max_length=100)
    full_name_en = models.CharField(max_length=100, null=True)
    code_name = models.CharField(max_length=50, null=True)
    administrative_unit = models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE, null=True, blank=True, default=None)
    administrative_region = models.ForeignKey(AdministrativeRegion, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return f'{self.code}.{self.code_name}'


class District(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=50, default=None)
    name_en = models.CharField(max_length=50, null=True)
    full_name = models.CharField(max_length=100)
    full_name_en = models.CharField(max_length=100, null=True)
    code_name = models.CharField(max_length=50, null=True)
    province_code = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, blank=True, default=None)
    administrative_unit = models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return f'{self.code}.{self.name}'


class Ward(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=50, default=None)
    name_en = models.CharField(max_length=50, null=True)
    full_name = models.CharField(max_length=100)
    full_name_en = models.CharField(max_length=100, null=True)
    code_name = models.CharField(max_length=50, null=True)
    district_code = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True, default=None)
    administrative_unit = models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return f'{self.code}.{self.name}'


class Location(models.Model):
    address = models.CharField(max_length=200)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, default=None)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.pk}'
