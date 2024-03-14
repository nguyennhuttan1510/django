from django.contrib.auth.models import User
from rest_framework import serializers, mixins, permissions, viewsets

# Create your views here.
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from common.exceptions.model import ResponseBase
from .permission import AuthorOrReadOnly, AccountAccessPolicy
from .serializers import ProfileSerializer
from .models import Profile


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AccountAccessPolicy]

    @action(detail=False, methods=['get'])
    def search(self, request):
        if request.query_params:
            items = Profile.objects.filter(**request.query_params.dict())
        else:
            items = Profile.objects.all()

        if items:
            serializer = self.get_serializer(items, many=True)
            return Response(ResponseBase(data=serializer.data, message='get users success').get())
        else:
            return Response(ResponseBase(message='not found').get(), status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def create_user(self, request, *args, **kwargs):
        email = request.data.get('email')
        print(email)
        if Profile.objects.filter(email=email).exists():
            return Response({'message': 'This data already exists'}, status=status.HTTP_400_BAD_REQUEST)
        return self.create(request, *args, **kwargs)

