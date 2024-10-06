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
        #Allow all users to read and create
        {
            "action": ["list", "create", "retrieve"],
            "principal": ['*'],
            "effect": "allow",
        },
        #Allow users is owner update
        {
            "action": ["partial_update", "update"],
            "principal": ["*"],
            "effect": "allow",
            "condition_expression": "is_author"

        },
        #Only owner is destroy
        {
            "action": ["destroy"],
            "principal": ["*"],
            "effect": "allow",
            "condition_expression": "is_author"
        },
    ]

    def is_author(self, request, view, action) -> bool:
        account = view.get_object()
        user = request.user or AnonymousUser()
        print(f'{user == account.creator}, {user}, {account.creator}')
        return user.id == account.owner_id
