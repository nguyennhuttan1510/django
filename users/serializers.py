from django.contrib.auth.models import User
from rest_framework import serializers

from authentication.serializers import UserSerializer
from organization.models import Organization
from users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    # organization = serializers.PrimaryKeyRelatedField(queryset=Organization)

    class Meta:
        model = Profile
        fields = '__all__'
