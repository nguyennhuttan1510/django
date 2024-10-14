from enum import Enum

from django.db import models


class TYPE_METADATA(Enum):
    SEX = 'SEX'
    CATEGORY_REVIEW = 'CATEGORY_REVIEW'
    RANK_POINT = 'RANK_POINT'


TYPE_CHOICES = [
    (TYPE_METADATA.SEX.value, TYPE_METADATA.SEX.name),
    (TYPE_METADATA.CATEGORY_REVIEW.value, TYPE_METADATA.CATEGORY_REVIEW.name),
    (TYPE_METADATA.RANK_POINT.value, TYPE_METADATA.RANK_POINT.name),
]


# Create your models here.
class Metadata(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    code = models.TextField()
    type = models.CharField(choices=TYPE_CHOICES, default=None, null=True, max_length=50)
    enabled = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
