from django.db import models


# Create your models here.
class Resource(models.Model):
    file = models.FileField(upload_to='file/')
