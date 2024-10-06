from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from common.exceptions.model import ResponseBase
from metadata.models import Metadata
from metadata.serializers import MetadataSerializer, MetadataDTOSerializer


# Create your views here.
class MetadataView(viewsets.ModelViewSet):
    queryset = Metadata.objects.all()
    serializer_class = MetadataSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        type = request.query_params.get('type', None)
        object = self.get_queryset().filter(type=type)
        serializer = MetadataDTOSerializer(object, many=True)
        return Response(ResponseBase(data=serializer.data, message=f'get sex option success').__dict__, status=status.HTTP_200_OK)