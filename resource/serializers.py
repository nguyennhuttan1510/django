from rest_framework import serializers

from resource.models import Resource, PrivateDocument, PublicDocument


class ResourceSerializer(serializers.ModelSerializer):
    # files = serializers.ListField(child=serializers.FileField())
    class Meta:
        model = Resource
        fields = '__all__'


class PrivateDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateDocument
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['file'] = rep.pop('upload')
        return rep


class PublicDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicDocument
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['file'] = rep.pop('upload')
        return rep
