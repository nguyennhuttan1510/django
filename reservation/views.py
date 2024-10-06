import json
import random
import smtplib

from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action

from common.exceptions.model import ResponseBase
from organization.models import Organization
from service.models import Service
from .models import Reservation
from .permission import ReservationPolicy
from .serializers import ReservationSerializer, StatusReservation


# Create your views here.
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [ReservationPolicy]

    @action(detail=False, methods=['get'])
    def search(self, request, *args, **kwargs):
        if request.query_params:
            items = Reservation.objects.filter(**request.query_params.dict())
        else:
            items = Reservation.objects.all()

        # if there is something in items else raise error
        if items:
            serializer = ReservationSerializer(items, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Reservation.objects.all()
        else:
            queryset = Reservation.objects.filter(Q(organization__owner__username=self.request.user.username) | Q(
                user__username=self.request.user.username) | Q(approved_by__username=self.request.user.username))

        serializer = ReservationSerializer(queryset, many=True)
        return Response(ResponseBase(serializer.data, message=f'get reservations of {request.user}').get())

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, many=False)
        return Response(ResponseBase(serializer.data, message=f'get reservation of {request.user}').get())

    def create(self, request, *args, **kwargs):
        try:
            # validate input
            if request.data['rooms'] is None or not isinstance(request.data['rooms'], list):
                return Response(
                    ResponseBase(message='rooms must be list').get(),
                    status=status.HTTP_400_BAD_REQUEST)

            # get rooms
            rooms = Service.objects.filter(pk__in=request.data['rooms'])

            # validate rooms have is one organization
            are_rooms_belong_organization = all(room.organization.pk == rooms[0].organization.pk for room in rooms)
            print(f'are_rooms_belong_organization: {are_rooms_belong_organization}')
            if not are_rooms_belong_organization:
                return Response(
                    ResponseBase(message='have some service is not belong to organization, please check again').get(),
                    status=status.HTTP_400_BAD_REQUEST)

            # check service is available
            is_exists = Reservation.objects.filter(status__in=[StatusReservation.ORDERED.name], rooms__in=request.data['rooms']).exists()
            print(f'is_exists: {is_exists}')
            if is_exists:
                return Response(
                    ResponseBase(message='have some rooms not available, please check again!').get(),
                    status=status.HTTP_400_BAD_REQUEST)

            # create reservation
            pin_code = random.randint(1000, 9999)

            reservation = ReservationSerializer(
                data={**request.data, 'user': request.user.id, 'organization': rooms[0].organization.pk, 'approved_by': rooms[0].organization.owner.pk,
                      'pin_code': pin_code}, many=False)

            # validate instance
            if reservation.is_valid():
                reservation.save(total_price=reservation.calculate_price())

                # self._send_mail_confirm_reservation({'pin_code': pin_code, 'reservation_id': reservation.data['id']})

                return Response(ResponseBase(data=reservation.data, message=f'create reservation').get(),
                                status=status.HTTP_201_CREATED)
            return Response(ResponseBase(reservation.errors, message='data invalid').get(),
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f'except: {e}')
            return Response(ResponseBase(message=f'create not success - {e}').get(), status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        res = super(ReservationViewSet, self).update(request, *args, **kwargs)
        if not res.data:
            return Response(ResponseBase(message='update reservation failed').get(), status=status.HTTP_400_BAD_REQUEST)
        return Response(ResponseBase(data=res.data, message='update reservation success').get(), status=status.HTTP_200_OK)

    def _send_mail_confirm_reservation(self, reservation):
        try:
            email = EmailMessage(
                        subject='Confirm your reservation',
                        body=f'Your pin code is {reservation["pin_code"]} and reservation id is {reservation["reservation_id"]}',
                        from_email='nguyentan15102000@gmail.com',
                        to=['nguyentan15102000@gmail.com']
                    )
            email.send()

        except Exception as e:
            print(f'except: {e}')
