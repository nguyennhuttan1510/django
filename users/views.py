import jwt
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import serializers, mixins, permissions, viewsets

# Create your views here.
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenVerifySerializer

from common.exceptions.model import ResponseBase
from .permission import AuthorOrReadOnly, AccountAccessPolicy
from .serializers import ProfileSerializer
from .models import Profile


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AccountAccessPolicy]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.query_params:
            items = Profile.objects.filter(**request.query_params.dict())
        else:
            items = queryset

        if items:
            serializer = self.get_serializer(items, many=True)
            return Response(ResponseBase(data=serializer.data, message='get users success').get())
        else:
            return Response(ResponseBase(message='not found').get(), status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(ResponseBase(data=serializer.data, message='get users success').get())
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ResponseBase(data=serializer.data, message='Profile successfully created'),
                        status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        try:
            res = super().partial_update(request, *args, **kwargs)
            return Response(ResponseBase(data=res.data, message='update profile successfully').get(),
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'data': None, 'message': 'update profile failed', 'cause': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
