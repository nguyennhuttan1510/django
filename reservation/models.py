import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from organization.models import Organization
from service.models import Service


# Create your models here.

class Reservation(models.Model):
    balance_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    check_in = models.DateTimeField(default=timezone.now)
    check_out = models.DateTimeField(default=timezone.now)
    guest = models.ForeignKey(User, related_name='guest', on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, related_name='organization', on_delete=models.CASCADE, default=None,
                                     null=True)
    approved_by = models.ForeignKey(User, related_name='approved_by', on_delete=models.CASCADE, default=None, null=True)
    services = models.ManyToManyField(Service, related_name='reservations', related_query_name='reservation')
    status = models.CharField(
        choices=[('ORDERED', 'ordered'), ('COMPLETED', 'completed'), ('CLOSE', 'close'), ('PENDING', 'pending'),
                 ('CANCEL', 'cancel')], default='ORDERED', max_length=30)
    is_active = models.BooleanField(default=True)
    pin_code = models.IntegerField(null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return str(f'{self.pk}_{self.guest.username}_{self.balance_amount}')
