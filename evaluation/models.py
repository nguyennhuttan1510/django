from enum import Enum

from django.db import models
from django.db.models import Count, Avg, Q, F, Value

from service.models import Service
from django.contrib.auth.models import User

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


class CATEGORY(Enum):
    CLEAN = 'CLEAN'
    POSITION = 'POSITION'
    VALUE = 'VALUE'
    CONVENIENT = 'CONVENIENT'
    SERVICE = 'SERVICE'


# Create your models here.
class Evaluation(models.Model):
    CATEGORY_CHOICES = [
        (CATEGORY.CLEAN.value, CATEGORY.CLEAN.name),
        (CATEGORY.POSITION.value, CATEGORY.POSITION.name),
        (CATEGORY.VALUE.value, CATEGORY.VALUE.name),
        (CATEGORY.CONVENIENT.value, CATEGORY.CONVENIENT.name),
        (CATEGORY.SERVICE.value, CATEGORY.SERVICE.name),
    ]
    title = models.CharField(max_length=100)
    description_satisfied = models.TextField(null=True, blank=True)
    description_unsatisfied = models.TextField(null=True, blank=True)
    points = models.IntegerField(default=0)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10, default=CATEGORY.CLEAN)
    user = models.ForeignKey(User, related_name="user_review", on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True, default=None,
                                related_name='evaluations')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return str(f'{self.pk}')


def get_evaluation_group_by_category(organization_id: int):
    evaluation_overview = list([])
    evaluations = Evaluation.objects.filter(service__organization__id=organization_id).values('category').annotate(
        count=Count('id'), point=Avg('points')).order_by('category')

    for category in CATEGORY:
        category_is_exist_in_evaluation = False

        for e in evaluations:
            if e['category'] == category.name:
                evaluation_overview.append(e)
                category_is_exist_in_evaluation = True
                break

        if category_is_exist_in_evaluation is False:
            context = {'category': category.name, 'count': 0, 'point': 0}
            evaluation_overview.append(context)

    return evaluation_overview
