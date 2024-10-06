from collections import OrderedDict

from rest_framework import serializers

from convenience.serializers import ConvenienceSerializer
from resource.serializers import ResourceSerializer, PrivateDocumentSerializer
from service.models import Service, evaluation_calc


class ServiceSerializer(serializers.ModelSerializer):
    conveniences = ConvenienceSerializer(many=True, read_only=True)
    name = serializers.CharField()
    # organization = OrganizationSerializer()
    # promotional_price = serializers.DecimalField(max_digits=20, decimal_places=2, default=0, read_only=True)
    # evaluations = EvaluationSerializer(many=True, read_only=True)
    # evaluation = serializers.SerializerMethodField()
    promotions = serializers.SerializerMethodField()
    resource = PrivateDocumentSerializer(many=True, read_only=True)
    promotional_price = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['id', 'name', 'type', 'status', 'description', 'price', 'capacity', 'promotional_price', 'rate', 'promotions',
                  'conveniences', 'resource', 'location']

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


class ServiceRepresentationSerializers(ServiceSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'promotional_price', 'capacity', 'rate']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['product_name'] = rep.pop('name')
        return rep
