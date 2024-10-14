import uuid
from datetime import timedelta
from enum import Enum
import random
from celery import shared_task

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from organization.models import Organization
from service.models import Service


class STATUS_RESERVATION(Enum):
    PENDING = 'PENDING'
    CONFIRMED = 'CONFIRMED'
    CANCEL = 'CANCEL'
    ORDERED = 'ORDERED'
    COMPLETED = 'COMPLETED'
    CLOSE = 'CLOSE'


STATUS_BOOKING_CHOICES = [
    (STATUS_RESERVATION.PENDING.value, STATUS_RESERVATION.PENDING.name),
    (STATUS_RESERVATION.CONFIRMED.value, STATUS_RESERVATION.CONFIRMED.name),
    (STATUS_RESERVATION.CANCEL.value, STATUS_RESERVATION.CANCEL.name),
    (STATUS_RESERVATION.ORDERED.value, STATUS_RESERVATION.ORDERED.name),
    (STATUS_RESERVATION.COMPLETED.value, STATUS_RESERVATION.COMPLETED.name),
    (STATUS_RESERVATION.CLOSE.value, STATUS_RESERVATION.CLOSE.name),
]


# Create your models here.

class Reservation(models.Model):
    total_price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    check_in = models.DateTimeField(default=timezone.now)
    check_out = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        choices=STATUS_BOOKING_CHOICES, default=None, max_length=30, null=True, blank=True)
    locked_until = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    pin_code = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, null=True)
    services = models.ManyToManyField(Service, related_name='reservations', related_query_name='reservation')

    objects = models.Manager()

    def __str__(self):
        return str(f'{self.pk}')

    def count_days(self):
        return (self.check_out - self.check_in).days


@shared_task
def check_and_cancel_booking(booking_id):
    try:
        booking = Reservation.objects.get(pk=booking_id)
        if booking.status == STATUS_RESERVATION.PENDING.value & timezone.now() > booking.locked_until:
            booking.status = STATUS_RESERVATION.CANCEL.value
            booking.locked_until = None
            booking.save()
    except Reservation.DoesNotExist:
        pass
