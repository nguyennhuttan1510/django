from rest_access_policy import AccessPolicy
from rest_access_policy.access_policy import AnonymousUser
from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        print(request.user)
        print(f'You have {request.method}, you have authenticated: {request.user.is_authenticated}')
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.created_by == request.user:
            return True
        return False


class AccountAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list"],
            "principal": ["admin", 'group:organization'],
            "effect": "allow",
        },
        {
            "action": ["retrieve", "partial_update", "update", "create_user"],
            "principal": ["admin", "group:organization", "group:staff"],
            "effect": "allow"
        },
        {
            "action": ["search"],
            "principal": ["admin", "group:organization"],
            "effect": "allow"
        },
        {
            "action": ["destroy"],
            "principal": ["admin", "group:organization", "group:staff"],
            "effect": "allow",
            "condition_expression": "is_author"
        },
    ]

    def is_author(self, request, view, action) -> bool:
        account = view.get_object()
        user = request.user or AnonymousUser()
        if user.is_superuser or user.is_staff:
            return True
        return user == account.created_by
