from django.db.models import Min, Avg, Q
from rest_framework import serializers
from convenience.serializers import ConvenienceSerializer
from evaluation.models import Evaluation, range_point, EVALUATION_FIELD, get_evaluation_group_by_category
from location.serializers import LocationSerializer
from organization.models import Organization
from resource.serializers import PrivateDocumentSerializer
from service.models import evaluation_calc, query_service, service_min_price
from service.serializers import ServiceSerializer, ServiceRepresentationSerializers


class OrganizationSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    location = LocationSerializer(read_only=True)
    evaluation = serializers.SerializerMethodField()
    conveniences = ConvenienceSerializer(many=True, read_only=True)
    resource = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        exclude = ['owner']
        extra_kwargs = {
            'resource': {'read_only': True}
        }

    def get_evaluation(self, instance):
        return OrganizationSearchSerializer(instance=instance).data['evaluation']

    def get_resource(self,instance):
        return OrganizationSearchSerializer(instance=instance).data['resource']


class OrganizationSearchSerializer(serializers.ModelSerializer):
    service_representation = serializers.SerializerMethodField()
    conveniences = ConvenienceSerializer(many=True)
    evaluation = serializers.SerializerMethodField()
    avg_price = serializers.SerializerMethodField()
    location = LocationSerializer(read_only=True)
    resource = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ['id', 'name', 'avg_price', 'location', 'phone', 'rate', 'evaluation', 'conveniences',
                  'service_representation', 'resource']

    def get_evaluation(self, instance):
        evaluations_services = Evaluation.objects.filter(service__organization=instance.id, is_active=True)
        point = round(evaluation_calc(evaluations_services), 2)

        evaluation_overview = get_evaluation_group_by_category(instance.id)
        return {
            'point': point,
            'count': len(evaluations_services),
            EVALUATION_FIELD.TYPE.value: range_point(point)[EVALUATION_FIELD.TYPE.value],
            # 'evaluations': evaluations.data,
            'evaluation_overview': evaluation_overview
        }

    def get_avg_price(self, instance):
        avg_price = instance.services.aggregate(Avg('price'))['price__avg']
        return format(avg_price, '.2f')

    def get_service_representation(self, instance):
        query = self.context.get('query', {})

        # QUERY PARAM
        capacity = query.get('capacity', None)
        organization_id = instance.pk
        # if existed start_date and end_date, system will query in reservation table to check available
        start_date = query.get('start_date', None)
        end_date = query.get('end_date', None)

        services = query_service(organization_id=organization_id, start_date=start_date, end_date=end_date, capacity=capacity)
        service = service_min_price(services)
        return ServiceRepresentationSerializers(service).data

    def get_resource(self, instance):
        services = instance.services.all()
        print('services', services)
        resources = list([])
        for service in services:
            resource = service.resource.all()
            resources.extend(resource)
        unique_resources = list(set(resources))
        return PrivateDocumentSerializer(unique_resources, many=True).data
