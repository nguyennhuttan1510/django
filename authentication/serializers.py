from django.contrib.auth.models import User
from rest_access_policy import FieldAccessMixin
from rest_framework import serializers

from authentication.permissions import AuthenticationPolicy


class UserSerializer(FieldAccessMixin, serializers.ModelSerializer):
    # old_password = serializers.CharField(required=True)
    # new_password = serializers.CharField(required=True)
    class Meta:
        model = User
        exclude = ['password']
        access_policy = AuthenticationPolicy
