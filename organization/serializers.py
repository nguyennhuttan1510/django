from collections import OrderedDict
from django.db.models import Min
from rest_framework import serializers
from convenience.serializers import ConvenienceSerializer
from evaluation.models import Evaluation, range_point, EVALUATION_FIELD
from evaluation.serializers import EvaluationSerializer
from organization.models import Organization
from service.models import evaluation_calc
from service.serializers import ServiceSerializer, ServiceRepresentationSerializers


class OrganizationSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True)
    service_representation = serializers.SerializerMethodField()
    conveniences = ConvenienceSerializer(many=True)
    evaluation = serializers.SerializerMethodField()
    avg_price = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ['id', 'name', 'avg_price', 'services', 'phone', 'rate', 'evaluation', 'conveniences', 'service_representation']

    def get_evaluation(self, instance):
        evaluations_services = Evaluation.objects.filter(service__organization=instance.id, is_active=True)
        point = round(evaluation_calc(evaluations_services), 2)

        def evaluation_template(representation, instance: Evaluation) -> dict:
            del representation['id']
            del representation['created_at']
            del representation['is_active']
            return representation

        evaluations = EvaluationSerializer(evaluations_services, many=True, context={'to_representation_template': evaluation_template})

        return {
            'point': point,
            'count': len(evaluations_services),
            EVALUATION_FIELD.TYPE.value: range_point(point)[EVALUATION_FIELD.TYPE.value],
            'evaluations': evaluations.data
        }

    def get_avg_price(self, instance):
        return format(instance.avg_price, '.2f')

    def get_service_representation(self, instance):
        request = self.context.get('request')
        capacity = request.query_params.get('capacity', None)

        services_filter = instance.services.filter()
        if capacity is not None:
            services_filter = services_filter.filter(capacity=capacity)

        cheapest_instance = services_filter.aggregate(Min('price'))['price__min']

        service = instance.services.filter(price=cheapest_instance).get()
        print('service', service)
        serializers_service = ServiceRepresentationSerializers(service)
        return serializers_service.data

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        del rep['services']
        result = OrderedDict(rep)
        return result
