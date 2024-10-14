from django.contrib.auth.models import User
from rest_framework import serializers

from authentication.serializers import UserSerializer
from organization.models import Organization
from users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class ProfileDTO(ProfileSerializer):
    class Meta(ProfileSerializer.Meta):
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'display_name', 'email']