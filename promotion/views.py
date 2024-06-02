from django.shortcuts import render
from rest_framework import viewsets

from promotion.models import Promotion
from promotion.serializers import PromotionSerializer


# Create your views here.
class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
