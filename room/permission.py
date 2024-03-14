from rest_access_policy import AccessPolicy
from rest_access_policy.access_policy import AnonymousUser


class RoomPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve", "search"],
            "principal": ["admin", "staff", "group:organization", "group:staff", "group:client"],
            "effect": "allow",
        },
        {
            "action": ["update", "partial_update", "destroy"],
            "principal": ["admin", "staff", "group:organization"],
            "effect": "allow",
            "condition": "is_owner"
        },
        {
            "action": ["create"],
            "principal": ["admin", "staff", "group:organization"],
            "effect": "allow",
        },
    ]

    def is_owner(self, request, view, action) -> bool:
        room = view.get_object()
        print(f'owner is {room.organization.owner}, user is {request.user}')
        user = request.user or AnonymousUser()
        if user.is_superuser or user.is_staff:
            return True
        return room.organization.owner == user


