from collections import OrderedDict

from rest_framework import serializers

from convenience.models import Convenience, TYPE_CONVENIENCE
from convenience.serializers import ConvenienceSerializer
from evaluation.models import EVALUATION_FIELD, range_point
from evaluation.serializers import EvaluationSerializer
from organization.serializers import OrganizationSerializer
from service.models import Service, evaluation_calc


class ServiceSerializer(serializers.ModelSerializer):
    conveniences = ConvenienceSerializer(many=True, read_only=True)
    organization = OrganizationSerializer()
    # promotional_price = serializers.DecimalField(max_digits=20, decimal_places=2, default=0, read_only=True)
    evaluations = EvaluationSerializer(many=True, read_only=True)
    evaluation = serializers.SerializerMethodField()
    promotions = serializers.SerializerMethodField()
    promotional_price = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'promotional_price', 'rate', 'promotions', 'organization',
                  'conveniences', 'evaluations', 'evaluation']
        depth = 2

    def get_evaluation(self, instance) -> dict:
        evaluations = instance.evaluations
        point = evaluation_calc(evaluations)
        return {
            'point': point,
            'count': len(evaluations),
            EVALUATION_FIELD.TYPE.value: range_point(point)[EVALUATION_FIELD.TYPE.value]
        }

    def get_promotional_price(self, instance) -> dict | None:
        promotional_price = instance.price_calc()
        if float(promotional_price) == float(instance.price):
            return None
        return promotional_price

    def get_promotions(self, instance) -> list:
        promotions = []
        for promotion in instance.promotions.all():
            print('promotion.promotions.all()', promotion.promotions.all())
            promotions.extend(promotion.promotions.all().values())
        return promotions

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        clone = OrderedDict(ret)
        ret.pop('name')
        ret.pop('evaluations')
        ret.pop('promotions')

        return {
            **ret,
            "evaluation": {
                **ret['evaluation'],
                "evaluations": clone['evaluations']
            },
            "promotions": clone['promotions'],
            "product_name": instance.name.upper(),
        }
