from django.contrib.auth.models import AnonymousUser
from rest_access_policy.access_policy import AccessPolicy

from reservation.models import Reservation
from reservation.serializers import StatusReservation


class EvaluationPolicy(AccessPolicy):
    statements = [
        {
            'action': ['retrieve', 'list'],
            'principal': ["*"],
            'effect': 'allow',
        },
        {
            'action': ['create'],
            'principal': ["*", 'anonymous'],
            'effect': 'allow',
            'condition': 'owner_of_reservation'
        },
        {
            'action': ['update', 'partial_update', 'destroy'],
            'principal': ["*"],
            'effect': 'allow',
            'condition': 'is_owner'
        },
    ]

    def is_owner(self, request, view, action) -> bool:
        evaluation = view.get_object()
        user = request.user or AnonymousUser()
        if user.is_superuser or user.is_staff:
            return True
        if request.data.get('pin_code') and request.data['reservation_id']:
            return True
        return evaluation.reservation.user.pk == request.user.pk

    def owner_of_reservation(self, request, view, action) -> bool:
        current_user = request.user
        if not current_user.is_authenticated:
            if request.data.get('pin_code'):
                pin_code = request.data['pin_code']
            else:
                pin_code = None
            payload = {
                'pin_code': pin_code,
                'pk': request.data['reservation'],
                # 'status': StatusReservation.COMPLETED.name
            }
        else:
            payload = {
                'user': current_user.pk,
                'pk': request.data['reservation'],
                # 'status': StatusReservation.COMPLETED.name
            }
        return Reservation.objects.filter(**payload).exists()
