from enum import Enum

from django.db import models
from django.db.models import Count, Avg, Q, F, Value

from metadata.models import Metadata
from reservation.models import Reservation
from service.models import Service
from django.contrib.auth.models import User


class RANGE_POINT(Enum):
    EXCELLENT = 9
    GREAT = 8
    RATHER = 7
    MEDIUM = 5
    BAD = 4
    VERY_BAD = 0


class RANK_CODE(Enum):
    EXCELLENT = 'EXCELLENT'
    GREAT = 'GREAT'
    QUITE = 'QUITE'
    MEDIUM = 'MEDIUM'
    BAD = 'BAD'
    WORSE = 'WORSE'


class CATEGORY(Enum):
    CLEAN = 'CLEAN'
    POSITION = 'POSITION'
    VALUE = 'VALUE'
    CONVENIENT = 'CONVENIENT'
    SERVICE = 'SERVICE'
    WIFI = 'WIFI'
    STAFF = 'STAFF'
    SATISFACTION = 'SATISFACTION'


# Create your models here.

CATEGORY_CHOICES = [
    (CATEGORY.CLEAN.value, CATEGORY.CLEAN.name),
    (CATEGORY.POSITION.value, CATEGORY.POSITION.name),
    (CATEGORY.VALUE.value, CATEGORY.VALUE.name),
    (CATEGORY.CONVENIENT.value, CATEGORY.CONVENIENT.name),
    (CATEGORY.SERVICE.value, CATEGORY.SERVICE.name),
]

RANK_CODE_CHOICES = [
    (RANK_CODE.EXCELLENT.value, RANK_CODE.EXCELLENT.name),
    (RANK_CODE.GREAT.value, RANK_CODE.GREAT.name),
    (RANK_CODE.QUITE.value, RANK_CODE.QUITE.name),
    (RANK_CODE.MEDIUM.value, RANK_CODE.MEDIUM.name),
    (RANK_CODE.BAD.value, RANK_CODE.BAD.name),
    (RANK_CODE.WORSE.value, RANK_CODE.WORSE.name),
]


class Evaluation(models.Model):
    title = models.CharField(max_length=100)
    description_satisfied = models.TextField(null=True, blank=True)
    description_unsatisfied = models.TextField(null=True, blank=True)
    points = models.IntegerField(default=0)
    rank_code = models.CharField(choices=RANK_CODE_CHOICES, max_length=10, default=None, blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10, default=CATEGORY.CLEAN.value)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, related_name="user_review", on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True, default=None,
                                related_name='evaluations')
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, blank=True, null=True,
                                    related_name='evaluations')

    objects = models.Manager()

    def __str__(self):
        return str(f'{self.pk}')


def get_evaluation_group_by_category(organization_id: int):
    evaluation_overview = list([])

    evaluations = Evaluation.objects.filter(service__organization__id=organization_id).values('category').annotate(
        count=Count('id'), point=Avg('points')).order_by('category')

    category_review_metadata = Metadata.objects.filter(type='CATEGORY_REVIEW')
    rank_name_metadata = Metadata.objects.filter(type='RANK_POINT')

    for category in CATEGORY:
        display_name = category_review_metadata.get(code=category.value).name or category.name
        evaluation_item = {
            'category': category.name,
            'display_name': display_name,
            'count': 0,
            'point': 0,
            'rank_name': None
        }
        for e in evaluations:
            if e['category'] == category.name:
                evaluation_item = {
                    **evaluation_item,
                    **e,
                    'point': round(e['point'], 2),
                    'rank_name': rank_name_metadata.get(code=get_rank_code(e['point'])).name
                }
                evaluation_overview.append(evaluation_item)
                break
            evaluation_overview.append({**evaluation_item, 'rank_name': rank_name_metadata.get(
                code=get_rank_code(evaluation_item['point'])).name})

    return evaluation_overview


def get_rank_code(point: float):
    if RANGE_POINT.EXCELLENT.value <= int(point) <= 10:
        return RANK_CODE.EXCELLENT.value
    elif RANGE_POINT.GREAT.value <= int(point) <= RANGE_POINT.EXCELLENT.value:
        return RANK_CODE.GREAT.value
    elif RANGE_POINT.RATHER.value <= int(point) <= RANGE_POINT.GREAT.value:
        return RANK_CODE.QUITE.value
    elif RANGE_POINT.MEDIUM.value <= int(point) <= RANGE_POINT.RATHER.value:
        return RANK_CODE.MEDIUM.value
    elif RANGE_POINT.BAD.value <= int(point) <= RANGE_POINT.MEDIUM.value:
        return RANK_CODE.BAD.value
    else:
        return RANK_CODE.WORSE.value
