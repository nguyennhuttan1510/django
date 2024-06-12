from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    def to_representation(self, instance) -> dict:
        to_representation_template = self.context.get('to_representation_template')
        rep = super().to_representation(instance)
        if to_representation_template:
            return to_representation_template(rep, instance)
        return rep