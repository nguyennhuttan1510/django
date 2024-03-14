from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, serializers, viewsets
from rest_framework.decorators import api_view, permission_classes, action

from common.exceptions.model import ResponseBase
from .models import Room
from .serializers import RoomSerializer
from .permission import RoomPolicy


# Create your views here.
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [RoomPolicy]

    @action(detail=False, methods=['get'])
    def search(self, request):
        if request.query_params:
            items = Room.objects.filter(**request.query_params.dict())
        else:
            items = Room.objects.all()

        if items:
            serializer = self.get_serializer(items, many=True)
            return Response(ResponseBase(data=serializer.data, message='get rooms success').get())
        else:
            return Response(ResponseBase(message='not found').get(), status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={**request.data, 'created_by': request.user.id})
        if serializer.is_valid():
            serializer.save()
            return Response(ResponseBase(data=serializer.data, message='create rooms success').get(), status=status.HTTP_201_CREATED)
        return Response(ResponseBase(serializer.errors, message='create rooms errors').get(), status=status.HTTP_400_BAD_REQUEST)
