from collections import OrderedDict

from rest_framework import serializers

from convenience.serializers import ConvenienceSerializer
from location.serializers import LocationSerializer
from resource.serializers import ResourceSerializer, PrivateDocumentSerializer, PublicDocumentSerializer
from service.models import Service, evaluation_calc, ServicesAssets


class ServiceAssetSerializers(serializers.ModelSerializer):
    service = serializers.StringRelatedField()
    asset = ConvenienceSerializer(many=False, read_only=True)

    class Meta:
        model = ServicesAssets
        fields = ['id', 'service', 'asset', 'quantity', 'created_at']


class ServiceSerializer(serializers.ModelSerializer):
    # conveniences = serializers.SerializerMethodField()
    # assets = ServiceAssetSerializers(source='servicesassets_set', many=True)
    name = serializers.CharField()
    # organization = OrganizationSerializer()
    # promotional_price = serializers.DecimalField(max_digits=20, decimal_places=2, default=0, read_only=True)
    # evaluations = EvaluationSerializer(many=True, read_only=True)
    # evaluation = serializers.SerializerMethodField()
    promotions = serializers.SerializerMethodField()
    resource = PublicDocumentSerializer(many=True, read_only=True)
    promotional_price = serializers.SerializerMethodField()
    assets = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['id', 'name', 'type', 'status', 'description', 'price', 'capacity', 'promotional_price', 'rate',
                  'promotions', 'conveniences', 'assets', 'resource']

    # def get_evaluation(self, instance) -> dict:
    #     evaluations = instance.evaluations
    #     point = evaluation_calc(evaluations)
    #     return {
    #         'point': point,
    #         'count': len(evaluations),
    #         EVALUATION_FIELD.TYPE.value: range_point(point)[EVALUATION_FIELD.TYPE.value]
    #     }

    def get_promotional_price(self, instance) -> dict | None:
        promotional_price = instance.price_calc()
        if float(promotional_price) == float(instance.price):
            return None
        return promotional_price

    def get_promotions(self, instance) -> list:
        return instance.promotions.all().values()

    # def get_conveniences(self, instance) -> list:
    #     conveniences = ConvenienceSerializer(instance.conveniences.all(), many=True, read_only=True)
    #     return [convenience for convenience in conveniences.data if convenience['type'] == 'CONVENIENCE']

    def get_assets(self, instance) -> list:
        data = list([])
        serializer = ServiceAssetSerializers(instance.servicesassets_set.all(), many=True)
        for asset in serializer.data:
            _data = asset.get('asset')
            _data['quantity'] = asset.get('quantity')
            data.append(_data)
        return data


class ServiceDTO(ServiceSerializer):
    class Meta(ServiceSerializer.Meta):
        fields = ['id', 'name', 'price', 'type', 'promotional_price', 'capacity', 'rate']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['product_name'] = rep.pop('name')
        return rep
