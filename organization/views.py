import datetime

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Min, Avg

from common.exceptions.model import ResponseBase
from organization.models import Organization
from organization.serializers import OrganizationSerializer, OrganizationSearchSerializer


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

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        # query by: capital, is_available_in_date, location
        end_date_default = datetime.datetime.now() + datetime.timedelta(days=2)

        capacity = request.query_params.get('capacity', 2)
        province_code = request.query_params.get('location', None)
        start_date = request.query_params.get('start_date', datetime.datetime.now())
        end_date = request.query_params.get('end_date', end_date_default)

        organization_filter = Organization.objects.filter(
            (
                    (Q(services__reservation__check_in__gte=end_date) | Q(
                        services__reservation__check_out__lte=start_date)) |
                    (Q(services__reservation__check_out__isnull=True) | Q(services__reservation__check_in__isnull=True))
            ) & Q(services__capacity=capacity) & Q(location__province__code=province_code)
        ).distinct()
        organizations = organization_filter

        serializer = OrganizationSearchSerializer(organizations, many=True, context={'request': request})
        return Response(ResponseBase(data=serializer.data, message='get organization successfully').get(),
                        status=status.HTTP_200_OK)

    # def list(self, request, *args, **kwargs):

