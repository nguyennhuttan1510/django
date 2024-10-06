from rest_framework import serializers
from location.models import Location


class LocationSerializer(serializers.ModelSerializer):
    full_address = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ['full_address']

    def get_full_address(self, instance):
        return f'{instance.address}, {instance.ward.full_name}, {instance.district.full_name}, {instance.province.full_name}'