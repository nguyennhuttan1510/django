from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from asset.models import AssetModel
from asset.serializers import AssetSerializer
from common.exceptions.model import ResponseBase


class AssetViewSet(viewsets.ModelViewSet):
    queryset = AssetModel.objects.all()
    serializer_class = AssetSerializer

    @action(['POST'], detail=False)
    def upload(self, request, pk=None):
        # asset_serializer = AssetSerializer(data=request.data)
        # asset_serializer.is_valid(raise_exception= True)
        # asset_serializer.save()
        # # file = asset_serializer.validated_data['asset']
        # # AssetModel.objects.create(file=file)
        print(f'File uploaded')
        return Response('success', status=status.HTTP_201_CREATED)
