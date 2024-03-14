from django.contrib.auth.models import User
from django.db import models

from reservation.models import Reservation
from room.models import Room


# Create your models here.
class Evaluation(models.Model):
    title = models.CharField(max_length=100)
    description_satisfied = models.TextField(null=True, blank=True)
    description_unsatisfied = models.TextField(null=True, blank=True)
    points = models.IntegerField(default=0)
    # guest = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='evaluations')
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE,null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f'{self.pk}')
