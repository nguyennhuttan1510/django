from django.core.exceptions import BadRequest
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from common.exceptions.model import ResponseBase
from evaluation.models import Evaluation
from evaluation.permissions import EvaluationPolicy
from evaluation.serializers import EvaluationSerializer, EvaluationDTO
from reservation.models import Reservation, STATUS_RESERVATION
from reservation.serializers import ReservationSerializer


# Create your views here.
class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [AllowAny]

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
        return Response(ResponseBase(data=EvaluationDTO(queryset, many=True).data, message='get evaluations success').get(),
                        status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        res = super().retrieve(request, *args, **kwargs)
        return Response(ResponseBase(data=res.data, message=f'get evaluations {self.kwargs["pk"]} success').get(),
                        status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        current_user = request.user
        pin_code = request.data['pin_code']
        booking_id = request.data['booking_id']
        print(f'current user: {current_user}')
        '''
            check user allow evaluated, must have reservation and status is COMPLETED
        '''
        try:
            if not current_user.is_authenticated:
                if not pin_code or not booking_id:
                    return Response(ResponseBase(message='pin code and booking not found', status=False))
                reservation = Reservation.objects.get(pin_code=pin_code, pk=booking_id,
                                                      status=STATUS_RESERVATION.COMPLETED.value)
            else:
                reservation = Reservation.objects.get(user=current_user.pk, pk=booking_id,
                                                      status=STATUS_RESERVATION.COMPLETED.value)
        except Exception as e:
            return Response(ResponseBase(message=str(e), status=False).get(),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        request.data['reservation'] = booking_id
        res = super().create(request, *args, **kwargs)
        reservation.status = STATUS_RESERVATION.CLOSE.value
        reservation.save()

        return Response(ResponseBase(data=res.data, message='post evaluation success').get(),
                        status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        res = super().update(request, *args, **kwargs)
        return Response(ResponseBase(data=res.data, message='update evaluation success').get(),
                        status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        res = super(EvaluationViewSet, self).destroy(request, *args, **kwargs)
        return Response(ResponseBase(message='delete evaluation success').get(), status=status.HTTP_204_NO_CONTENT)
