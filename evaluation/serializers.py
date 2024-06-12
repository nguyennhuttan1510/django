from rest_framework import serializers

from common.serializers.base_serializer import BaseSerializer
from evaluation.models import Evaluation
from reservation.serializers import ReservationSerializer


class EvaluationSerializer(serializers.ModelSerializer, BaseSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'

    def calculate_score(self) -> float:
        print(f'self: {self}')
