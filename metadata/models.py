from django.db import models


# Create your models here.
class Metadata(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    code = models.TextField()
    type = models.CharField(max_length=50)
    enabled = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
