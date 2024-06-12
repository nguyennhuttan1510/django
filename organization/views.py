import datetime

from rest_framework import status, viewsets
from rest_framework.response import Response
from django.db.models import Q, Min, Avg

from common.exceptions.model import ResponseBase
from organization.models import Organization
from organization.serializers import OrganizationSerializer


# Create your views here.
class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    # def get_queryset(self):
    #     is_admin = self.request.user.is_superuser
    #     print('is_admin', is_admin)
    #     if is_admin:
    #         return Organization.objects.all()
    #     else:
    #         return Organization.objects.filter(created_by=self.request.user)

    def list(self, request, *args, **kwargs):
        # query by: capital, is_available_in_date, location
        end_date_default = datetime.datetime.now() + datetime.timedelta(days=2)

        capacity = request.query_params.get('capacity', 2)
        location = request.query_params.get('location', None)
        start_date = request.query_params.get('start_date', datetime.datetime.now())
        end_date = request.query_params.get('end_date', end_date_default)

        # start_date = request.query_params.get('start_date', '2024-06-12')
        # end_date = request.query_params.get('end_date', '2024-06-14')


        organization_filter = Organization.objects.filter(
            (
                (Q(services__reservation__check_in__gte=end_date) | Q(services__reservation__check_out__lte=start_date)) |
                (Q(services__reservation__check_out__isnull=True) | Q(services__reservation__check_in__isnull=True))
            ) & Q(services__capacity=capacity)
        ).distinct()
        print('filter date', organization_filter)
        organization_filter = organization_filter.annotate(avg_price=Avg('services__price'))
        organizations = organization_filter
        # organizations = organizations_with_avg_price.filter(services__capacity=capacity)

        if location is not None:
            organizations = organization_filter.filter(location=location)
        # if start_date is not None:
        #     organizations = organizations_with_avg_price.filter(services__reservations__check_in__range=['2024-05-01', '2024-06-30'])
        # if end_date is not None:
        #     organizations = organizations_with_avg_price.filter(location=location)

        print('organizations', organizations)
        serializer = OrganizationSerializer(organizations, many=True, context={'request': request})
        return Response(ResponseBase(data=serializer.data, message='get organization successfully').get(),
                        status=status.HTTP_200_OK)
