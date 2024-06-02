from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from common.exceptions.model import ResponseBase
from convenience.models import Convenience
from convenience.serializers import ConvenienceSerializer


# Create your views here.
@api_view(['GET'])
def view_conveniences(request, pk=None):
    if pk is not None:
        obj = get_object_or_404(Convenience, pk=pk)
        instance = ConvenienceSerializer(obj, many=False).data
        return Response(instance, status=status.HTTP_200_OK)

    if request.query_params:
        items = ConvenienceSerializer.objects.filter(**request.query_params.dict())
    else:
        items = Convenience.objects.all()

    if items:
        instance = ConvenienceSerializer(items, many=True).data
        return Response(ResponseBase(data=instance, message='get category success').get(), status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)