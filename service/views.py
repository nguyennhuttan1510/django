import dataclasses
import datetime
from decimal import Decimal
from typing import List

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status, serializers, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.utils import json

from common.exceptions.model import ResponseBase
from evaluation.models import Evaluation
# from reservation.models import get_evaluation
from reservation.serializers import ReservationSerializer
from .models import Service, query_service
from .serializers import ServiceSerializer
from .permission import ServicePolicy


# Create your views here.
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [ServicePolicy]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # QUERY PARAM
        capacity = request.query_params.get('capacity', None)
        organization_id = request.query_params.get('organization_id', None)
        # if existed start_date and end_date, system will query in reservation table to check available
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        try:
            queryset = query_service(organization_id=organization_id, start_date=start_date, end_date=end_date,
                                     capacity=capacity)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'get service unsuccessful'})

        if queryset.count() == 0:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'not found', 'data': []})

        serializer = self.get_serializer(queryset, many=True)
        return Response(ResponseBase(data=serializer.data, message='get services success').get(),
                        status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        res = super().retrieve(request, *args, **kwargs)
        if res and res.data:
            return Response(ResponseBase(data=res.data, message='get product success', status=True).get(),
                            status=status.HTTP_200_OK)
        return Response(ResponseBase(message='get error', status=False).get(), status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={**request.data, 'created_by': request.user.id})
        if serializer.is_valid():
            serializer.save()
            return Response(ResponseBase(data=serializer.data, message='create rooms success').get(),
                            status=status.HTTP_201_CREATED)
        return Response(ResponseBase(serializer.errors, message='create rooms errors').get(),
                        status=status.HTTP_400_BAD_REQUEST)
