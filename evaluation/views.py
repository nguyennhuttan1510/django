from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from common.exceptions.model import ResponseBase
from evaluation.models import Evaluation
from evaluation.permissions import EvaluationPolicy
from evaluation.serializers import EvaluationSerializer
from reservation.models import Reservation
from reservation.serializers import ReservationSerializer, StatusReservation


# Create your views here.
class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [EvaluationPolicy, AllowAny]

    def list(self, request, *args, **kwargs):
        # QUERY PARAMS
        organization_id = request.query_params.get('organization_id', None)
        service_id = request.query_params.get('service_id', None)
        point = request.query_params.get('point', None)

        queryset = self.get_queryset()
        if organization_id:
            queryset = queryset.filter(service__organization=organization_id)
        if service_id:
            queryset = queryset.filter(service=service_id)
        if (organization_id or service_id) and point:
            queryset = queryset.filter(points=point)
        serializer = self.get_serializer(queryset, many=True)
        return Response(ResponseBase(data=serializer.data, message='get evaluations success').get(),
                        status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        res = super(EvaluationViewSet, self).retrieve(request, *args, **kwargs)
        return Response(ResponseBase(data=res.data, message=f'get evaluations {self.kwargs["pk"]} success').get(),
                        status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        current_user = request.user
        print(f'current user: {current_user}')
        '''
            check user allow evaluated, must have reservation and status is COMPLETED
        '''
        try:
            if not current_user.is_authenticated:
                reservation = Reservation.objects.get(pin_code=request.data['pin_code'], pk=request.data['reservation'],
                                                      status=StatusReservation.COMPLETED.name)
            else:
                reservation = Reservation.objects.get(user=current_user.pk, pk=request.data['reservation'],
                                                      status=StatusReservation.COMPLETED.name)
        except Exception as e:
            print(f'Exception: {e}')
            return Response(ResponseBase(message=f"you have not been evaluate reservation yet - {e}").get(),
                            status=status.HTTP_400_BAD_REQUEST)

        res = super(EvaluationViewSet, self).create(request, *args, **kwargs)
        reservation.status = StatusReservation.CLOSE.name
        reservation.save()

        return Response(ResponseBase(data=res.data, message='post evaluation success').get(),
                        status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        res = super().update(request, *args, **kwargs)
        return Response(ResponseBase(data=res.data, message='update evaluation success').get(),
                        status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        res = super(EvaluationViewSet, self).destroy(request, *args, **kwargs)
        return Response(ResponseBase(message='delete evaluation success').get(), status=status.HTTP_204_NO_CONTENT)
