from django.db import models



# Create your models here.
class Country(models.Model):
    country_name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.country_name}'


class City(models.Model):
    city_name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.city_name}'


class District(models.Model):
    district_name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.district_name}'


class Ward(models.Model):
    ward_name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.ward_name}'


class Location(models.Model):
    location_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=2)
    longitude = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return f'{self.pk}'



