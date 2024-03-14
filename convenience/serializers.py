from rest_framework import serializers

from convenience.models import Convenience


class ConvenienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Convenience
        fields = '__all__'
