from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


# Create your models here.


class Profile(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    display_name = models.CharField(max_length=100, null=True, blank=True)
    birthday = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=10, default="")
    address = models.CharField(max_length=300, null=True, blank=True)
    sex = models.CharField( max_length=1, choices=SEX_CHOICES, default="F")
    national_id = models.CharField(max_length=12, null=True, blank=True)
    nation = models.CharField(null=True, blank=True, max_length=3)
    owner = models.ForeignKey(User, related_name='profile_owner', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name='profile_creator', on_delete=models.CASCADE, null=True, blank=True)
    objects = models.Manager()

    def clean(self):
        super().clean();
        if self.birthday > timezone.now():
            raise ValidationError('birthday cannot be greater than now')


    def __str__(self):
        return str(f'{self.email}')
