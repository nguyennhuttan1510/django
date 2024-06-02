import dataclasses
from decimal import Decimal
from typing import List

from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status, serializers, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.utils import json

from common.exceptions.model import ResponseBase
from convenience.models import Convenience, TYPE_CONVENIENCE
from evaluation.models import Evaluation
# from reservation.models import get_evaluation
from reservation.serializers import ReservationSerializer
from .models import Service, evaluation_calc
from .serializers import ServiceSerializer
from .permission import RoomPolicy


# Create your views here.
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [RoomPolicy]

    def get_queryset(self):
        is_admin = self.request.user.is_superuser
        print('is_admin', is_admin)
        if is_admin:
            return Service.objects.all()
        else:
            return Service.objects.filter(created_by=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.query_params:
            services: List[Service] = queryset.filter(**request.query_params.dict())
        else:
            services: List[Service] = queryset

        for service in services:
            service.evaluations = Evaluation.objects.select_related('service').filter(service=service.pk)

        if services:
            serializer = self.get_serializer(services, many=True)
            return Response(ResponseBase(data=serializer.data, message='get services success').get(), status=status.HTTP_200_OK)
        else:
            return Response(ResponseBase(message='not found').get(), status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={**request.data, 'created_by': request.user.id})
        if serializer.is_valid():
            serializer.save()
            return Response(ResponseBase(data=serializer.data, message='create rooms success').get(),
                            status=status.HTTP_201_CREATED)
        return Response(ResponseBase(serializer.errors, message='create rooms errors').get(),
                        status=status.HTTP_400_BAD_REQUEST)
