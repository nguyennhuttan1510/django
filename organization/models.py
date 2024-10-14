from django.contrib.auth.models import User
from django.db import models

from convenience.models import Convenience
from location.models import Location

TYPE_ACCOMMODATION = [
    ("APARTMENT", "Apartment"),
    ("VILLA", "Villa"),
    ("HOSTEL", "Hostel"),
    ("LODGE", "Lodge"),
    ("STUDIO", "Studio"),
    ("VACATION_HOME", "Vacation Home"),
    ("BUNGALOW", "Bungalow"),
    ("CHALET", "Chalet"),
]


# Create your models here.
class Organization(models.Model):
    name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=11, unique=True, null=False, blank=False)
    organization_type = models.CharField(choices=TYPE_ACCOMMODATION, max_length=20, null=True, blank=True)
    status = models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=30)
    description = models.TextField(max_length=500, null=True, blank=True)
    rate = models.FloatField(default=0, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organization', default=None, null=True)
    location = models.OneToOneField(Location, on_delete=models.CASCADE, null=True, blank=True, default=None)
    conveniences = models.ManyToManyField(Convenience, blank=True, null=True, default=None,
                                          related_name='organizations')

    objects = models.Manager()

    def __str__(self):
        return self.name
