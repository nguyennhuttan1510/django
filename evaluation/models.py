from enum import Enum

from django.db import models
from service.models import Service


class RANGE_POINT(Enum):
    EXCELLENT = 9
    GREAT = 8
    RATHER = 7
    MEDIUM = 5
    BAD = 4
    VERY_BAD = 0


class EVALUATION_FIELD(Enum):
    TYPE = 'rank_name'
    POINTS = 'points'


def range_point(point: float):
    if RANGE_POINT.EXCELLENT.value <= int(point) <= 10:
        range = {
            EVALUATION_FIELD.TYPE.value: 'Xuất sắc',
            EVALUATION_FIELD.POINTS.value: point
        }
    elif RANGE_POINT.GREAT.value <= int(point) <= RANGE_POINT.EXCELLENT.value:
        range = {
            EVALUATION_FIELD.TYPE.value: 'Tuyệt vời',
            EVALUATION_FIELD.POINTS.value: point
        }
    elif RANGE_POINT.RATHER.value <= int(point) <= RANGE_POINT.GREAT.value:
        range = {
            EVALUATION_FIELD.TYPE.value: 'Khá',
            EVALUATION_FIELD.POINTS.value: point
        }
    elif RANGE_POINT.MEDIUM.value <= int(point) <= RANGE_POINT.RATHER.value:
        range = {
            EVALUATION_FIELD.TYPE.value: 'Trung bình',
            EVALUATION_FIELD.POINTS.value: point
        }
    elif RANGE_POINT.BAD.value <= int(point) <= RANGE_POINT.MEDIUM.value:
        range = {
            EVALUATION_FIELD.TYPE.value: 'tệ',
            EVALUATION_FIELD.POINTS.value: point
        }
    else:
        range = {
            EVALUATION_FIELD.TYPE.value: 'Rất tệ',
            EVALUATION_FIELD.POINTS.value: point
        }
    return range

# Create your models here.
class Evaluation(models.Model):
    title = models.CharField(max_length=100)
    description_satisfied = models.TextField(null=True, blank=True)
    description_unsatisfied = models.TextField(null=True, blank=True)
    points = models.IntegerField(default=0)
    # guest = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return str(f'{self.pk}')

