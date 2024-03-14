from rest_access_policy import AccessPolicy
from rest_framework import permissions

from users.models import Profile


class AuthenticationPolicy(AccessPolicy):
    statements = [
        {
            'action': ['list'],
            'principal': ['admin', 'staff'],
            'effect': 'allow'
        },
        {
            'action': ['retrieve', 'update', 'partial_update'],
            'principal': ['admin', 'staff', 'group:organization', 'group:staff', 'group:client', 'authenticated'],
            'effect': 'allow',
            'condition_expression': ["(is_owner or is_creator)"]
        },
        {
            'action': ['create'],
            'principal': ['admin', 'staff', 'group:organization', 'group:staff', 'group:client', 'anonymous'],
            'effect': 'allow',
        },
        # {
        #     'action': ['assign_group'],
        #     'principal': ['admin', 'staff', 'group:organization', 'group:staff', 'group:client'],
        #     'effect': 'allow',
        # },
        {
            'action': ['destroy'],
            'principal': ['admin', 'staff', 'group:organization', 'group:staff', 'group:client', 'authenticated'],
            'effect': 'allow',
            'condition_expression': ["(is_owner or is_creator)"]
        },
    ]

    def is_owner(self, request, view, action) -> bool:
        req_user = request.user
        user = view.get_object()
        if req_user.is_superuser or req_user.is_staff:
            return True
        return user.pk == req_user.pk

    def is_creator(self, request, view, action) -> bool:
        req_user = request.user
        user = view.get_object()
        profile = Profile.objects.get(owner=user.pk)
        return profile.creator.pk == req_user.pk


    @classmethod
    def scope_fields(cls, request, fields: dict, instance=None) -> dict:
        user = request.user
        if user.is_superuser or user.is_staff:
            return fields
        fields['is_superuser'].read_only = True
        fields['is_active'].read_only = True
        fields['is_staff'].read_only = True
        return fields
