import datetime
import logging

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Min, Avg

from common.exceptions.model import ResponseBase
from organization.models import Organization
from organization.serializers import OrganizationSerializer, OrganizationSearchSerializer

logger = logging.getLogger(__name__)


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
        queryset = self.get_queryset()
        # query by: capital, is_available_in_date, location
        # end_date_default = datetime.datetime.now() + datetime.timedelta(days=2)

        # QUERY PARAM
        capacity = request.query_params.get('capacity', 2)
        province_code = request.query_params.get('location', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        try:
            if province_code:
                queryset = queryset.filter(location__province__code=province_code)
            if capacity:
                queryset = queryset.filter(services__capacity=capacity)
            if start_date:
                queryset = queryset.filter(
                    Q(services__reservation__check_out__lte=start_date) | Q(
                        services__reservation__check_out__isnull=True))
            if end_date:
                queryset = queryset.filter(
                    Q(services__reservation__check_in__gte=end_date) | Q(services__reservation__check_in__isnull=True))
            queryset = queryset.distinct()
        except Exception as e:
            logger.error(f'search organization error: {e}')
            return Response(data={'message': 'not found', 'cause': e, 'data': []}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrganizationSearchSerializer(queryset, many=True,
                                                  context={'query': {'capacity': capacity, 'start_date': start_date,
                                                                     'end_date': end_date}})
        return Response(ResponseBase(data=serializer.data, message='get organization successfully').get(),
                        status=status.HTTP_200_OK)
