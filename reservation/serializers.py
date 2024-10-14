from enum import Enum

from rest_framework import serializers

from authentication.serializers import UserSerializer
from reservation.models import Reservation
from service.serializers import ServiceSerializer, ServiceDTO
from users.models import Profile
from users.serializers import ProfileSerializer, ProfileDTO


class ReservationSerializer(serializers.ModelSerializer):
    # guest = AccountSerializer(read_only=True)
    # services = ServiceSerializer(read_only=True, many=True)
    class Meta:
        model = Reservation
        fields = '__all__'

    def calculate_price(self):
        print(f'self.rooms: {self.validated_data["rooms"]}')
        rooms = self.validated_data["rooms"]
        if rooms is None:
            return
        total = 0
        if len(rooms) > 0:
            print(f'calculate_price__rooms : {rooms}')
            total = sum([room.price for room in rooms])
            print(f'calculate_price__total : {total}')
        return total

    # def check_existed(*args, **kwargs) -> bool:
    #     print(f'args - kwargs : {args} - {kwargs}')
    #     return Reservation.objects.filter(**kwargs).exists()

    # def get(self, *args, **kwargs):
    #     return Reservation.objects.get(**kwargs)

    # def has_reservation_with_status(self, request, status=None, *args, **kwargs):
    #     payload = self.get_query(request)
    #     if status:
    #         payload['status'] = status
    #     print(f'payload : {payload}')
    #     return self.check_existed(**payload)
    #
    # def get_query(self, request, *args, **kwargs):
    #     current_user = request.user
    #     # validate for unauthenticated
    #     if current_user is None or not current_user.is_authenticated:
    #         pin_code = request.data.get('pin_code')
    #         reservation_id = request.data.get('reservation_id')
    #         payload = {'pk': reservation_id, 'pin_code': pin_code}
    #
    #     # validate for authenticated
    #     else:
    #         payload = {
    #             'guest': current_user.pk,
    #             'rooms': request.data.get('service'),
    #         }
    #     return payload

    # def change_status(self, request, *args, **kwargs):
    #     payload = self.get_query(request=request, *args, **kwargs)
    #     if kwargs['status'] == 'COMPLETED':
    #         payload['status'] = 'END_PROCESS'
    #
    #     reservation_data = self.get(**payload)
    #     print(f'reservation_data: {reservation_data}')
    #
    #     reservation_data.status = kwargs['status']
    #     reservation_data.save()


class ReservationDTO(ReservationSerializer):
    check_in = serializers.DateTimeField(required=True)
    check_out = serializers.DateTimeField(required=True)
    services = ServiceDTO(read_only=True, many=True, required=False)
    user = serializers.SerializerMethodField(required=False)

    class Meta(ReservationSerializer.Meta):
        fields = ['id', 'check_in', 'check_out', 'status', 'created_at', 'user', 'services']

    def get_user(self, instance):
        profile = Profile.objects.get(owner=instance.user)
        return ProfileDTO(profile).data

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['count_day'] = Reservation.objects.get(pk=instance.pk).count_days()
        return rep
