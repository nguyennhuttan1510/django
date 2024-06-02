from rest_framework import serializers
from asset.models import AssetModel


# Create your views here.
class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetModel
        fields = '__all__'