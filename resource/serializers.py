from rest_framework import serializers

from resource.models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    # files = serializers.ListField(child=serializers.FileField())
    class Meta:
        model = Resource
        fields = '__all__'
