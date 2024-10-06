from rest_framework import serializers

from metadata.models import Metadata


class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metadata
        fields = '__all__'


class MetadataDTOSerializer(serializers.Serializer):
    name = serializers.CharField()
    code = serializers.CharField()
    description = serializers.CharField()
