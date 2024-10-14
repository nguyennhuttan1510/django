import datetime
import logging

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Min, Avg

from common.exceptions.model import ResponseBase
from organization.models import Organization
from organization.serializers import OrganizationSerializer, OrganizationSearchSerializer, \
    OrganizationSearchParamsSerializer
from reservation.models import Reservation
from service.models import Service

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
    @action(methods=['get'], detail=False,
            url_path='search-available-room', url_name='search_available_organization')
    def search_organization_have_room_available(self, request, *args, **kwargs):
        available_organizations = []
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        capacity = request.query_params.get('capacity', None)
        province = request.query_params.get('province_code', None)

        #Validate query params
        OrganizationSearchParamsSerializer(data=request.query_params).is_valid(raise_exception=True)

        # Find all booked room during the request date
        booked_room = Reservation.objects.filter(
            Q(check_in__lt=end_date) & Q(check_out__gt=start_date)
        ).values_list('services', flat=True)
        available_rooms = Service.objects.exclude(pk__in=booked_room)

        #Find all rooms have capacity greater than or equal in the list available rooms
        available_rooms = available_rooms.filter(capacity__gte=capacity)

        # Find all rooms have capacity greater than or equal in the list available rooms
        available_rooms = available_rooms.filter(organization__location__province=province)

        available_organizations = Organization.objects.filter(services__in=available_rooms).distinct()
        return Response(
            ResponseBase(data=OrganizationSerializer(available_organizations, many=True).data, message='search organization have room available successfully').get(), status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
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

    def retrieve(self, request, *args, **kwargs):
        try:
            res = super().retrieve(request, *args, **kwargs)
            return Response(ResponseBase(data=res.data, message='get organization success', status=True).get(), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(ResponseBase(message=f'get organization failed: {str(e)}', status=False).get(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)





