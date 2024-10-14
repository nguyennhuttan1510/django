from django.db import models

from tutorial.storage_backends import PrivateMediaStorage, PublicMediaStorage


# Create your models here.
class Resource(models.Model):
    file = models.FileField(upload_to='file/')


# class Document(models.Model):
class PrivateDocument(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField(storage=PrivateMediaStorage())

    # user = models.ForeignKey(User, related_name='documents', on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.pk}'


class PublicDocument(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField(storage=PublicMediaStorage())

    def __str__(self):
        return f'{self.pk}'
