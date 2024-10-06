from decimal import Decimal
from typing import List

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q, Min

from convenience.models import Convenience
from location.models import Location
from organization.models import Organization
from promotion.models import Promotion
from resource.models import Resource, PrivateDocument


# Create your models here.

TYPE_ACCOMMODATION = [
    ("APARTMENT", "Apartment"),
    ("VILLA", "Villa"),
    ("HOSTEL", "Hostel"),
    ("LODGE", "Lodge"),
    ("STUDIO", "Studio"),
    ("VACATION_HOME", "Vacation Home"),
    ("BUNGALOW", "Bungalow"),
    ("CHALET", "Chalet"),
]

class Service(models.Model):
    name = models.CharField(max_length=100)
    sub_name: models.CharField(max_length=100)
    description = models.TextField(max_length=300, null=True, blank=True)
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    type = models.CharField( choices=TYPE_ACCOMMODATION, max_length=20, null=True, blank=True)
    status = models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=30)
    conveniences = models.ManyToManyField(Convenience, null=True, blank=True, through='ServicesAssets')
    rate = models.FloatField(default=0, null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True, related_name='services', on_delete=models.CASCADE, default=None)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     default=None, null=True, related_name='services')
    promotions = models.ManyToManyField(Promotion, blank=True, null=True)
    resource = models.ManyToManyField(PrivateDocument, null=True, blank=True)
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


def query_service(organization_id, capacity, start_date, end_date):
    queryset = Service.objects.all()
    if organization_id:
        queryset = queryset.filter(organization=organization_id)
    if capacity:
        queryset = queryset.filter(capacity=capacity)
    if start_date:
        queryset = queryset.filter(Q(reservation__check_out__lte=start_date) | Q(reservation__check_in__isnull=True))
    if end_date:
        queryset = queryset.filter(Q(reservation__check_in__gte=end_date) | Q(reservation__check_out__isnull=True))
    return queryset


def service_min_price(services):
    return min(services, key=lambda x: x.price)


class ServicesAssets(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    asset = models.ForeignKey(Convenience, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
