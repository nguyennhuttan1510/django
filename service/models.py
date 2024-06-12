from decimal import Decimal
from typing import List

from django.contrib.auth.models import User
from django.db import models

from convenience.models import Convenience
from organization.models import Organization
from convenience.models import TYPE_CONVENIENCE
from promotion.models import Promotion


# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     default=None, null=True, related_name='services')
    conveniences = models.ManyToManyField(Convenience)
    rate = models.DecimalField(default=0, max_digits=5, decimal_places=1)
    promotions = models.ManyToManyField(Promotion)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    objects = models.Manager()

    def price_calc(self) -> Decimal:
        print('self', self.promotions.all())
        price = Decimal(self.price)
        promotions_service = self.promotions.all()
        promotion_items = []
        for promotion in promotions_service:
            promotion_items.extend(promotion.promotions.all())
        if promotion_items:
            for promotion in promotion_items:
                price += (Decimal(promotion.discount) * Decimal(self.price) / 100)
        return price

    def __str__(self):
        return self.name


def evaluation_calc(evaluations: list) -> float:
    agv_point = 0
    print('evaluations', evaluations)
    for evaluation in evaluations:
        print('evaluation', evaluation)
        agv_point += int(evaluation.points)
    if agv_point == 0:
        return agv_point
    return agv_point / len(evaluations)
