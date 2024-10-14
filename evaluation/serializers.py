from rest_framework import serializers

from authentication.serializers import UserSerializer
from common.serializers.base_serializer import BaseSerializer
from evaluation.models import Evaluation, get_rank_code
from metadata.models import Metadata
from reservation.serializers import ReservationSerializer, ReservationDTO


class EvaluationSerializer(serializers.ModelSerializer, BaseSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'

    def create(self, validated_data):
        point = validated_data['points']
        evaluation = Evaluation.objects.create(**validated_data, rank_code=get_rank_code(point))
        return evaluation


class EvaluationDTO(EvaluationSerializer):
    reservation = ReservationDTO(read_only=True)

    # title = serializers.CharField()
    # points = serializers.IntegerField()
    # rank_code = serializers.CharField()
    # category = serializers.CharField()
    # description_satisfied = serializers.CharField()
    # description_unsatisfied = serializers.CharField()
    class Meta(EvaluationSerializer.Meta):
        fields = ['title', 'reservation', 'points', 'rank_code', 'category', 'description_satisfied',
                  'description_unsatisfied', 'created_at']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['rank_name'] = Metadata.objects.get(code=rep['rank_code']).name
        rep['category_name'] = Metadata.objects.get(code=rep['category']).name
        return rep
