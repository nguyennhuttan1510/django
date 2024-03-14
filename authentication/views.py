import json

from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from authentication.permissions import AuthenticationPolicy
from authentication.serializers import UserSerializer
from common.exceptions.model import ResponseBase
from users.serializers import ProfileSerializer


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AuthenticationPolicy]

    def create(self, request, *args, **kwargs):
        # check username is unique
        has_user = User.objects.filter(username=request.data['username']).exists()
        if has_user:
            return Response(ResponseBase(message='User already exists.').get(), status=status.HTTP_400_BAD_REQUEST)

        # create user
        new_user = User.objects.create_user(username=request.data['username'], password=request.data['password'])
        if new_user is not None:
            '''
            assign user to group lower level than creator.
            else new user will be client group.
            
            create profile for new user.
            '''
            new_user = self._assign_group_to(request, new_user)

            profile_new_user = ProfileSerializer(data={"owner": new_user.pk, 'creator': request.user.pk})
            profile_new_user.is_valid(raise_exception=True)
            profile_new_user.save()

            serializer = UserSerializer(new_user, context={'request': request})
            return Response(ResponseBase(data=serializer.data, message='create user success').get(),
                            status=status.HTTP_201_CREATED)
        return Response(ResponseBase(message='create error').get(), status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        res = super().retrieve(self, request, *args, **kwargs)
        print(f'result: {res.data}')
        if res and res.data:
            return Response(ResponseBase(data=res.data, message='get user success').get(), status=status.HTTP_200_OK)
        return Response(ResponseBase(message='get error').get(), status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        res = super().update(request, *args, **kwargs)
        print(f'result: {res.data}')
        if res and res.data:
            return Response(ResponseBase(data=res.data, message='update user success').get(), status=status.HTTP_200_OK)
        return Response(ResponseBase(message='update error').get(), status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        res = super().destroy(request, args, kwargs)
        if res.data:
            return Response(ResponseBase(data=res.data, message='delete user success').get(), status=status.HTTP_200_OK)
        return Response(ResponseBase(message='delete error').get(), status=status.HTTP_400_BAD_REQUEST)

    def _assign_group_to(self, request, user, *args, **kwargs):
        if request.user.groups.filter(name='organization').exists():
            group = Group.objects.get(name='staff')
            user.groups.add(group)

        if not request.user.is_authenticated:
            group = Group.objects.get(name='client')
            user.groups.add(group)
        return user
