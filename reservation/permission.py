from rest_access_policy import AccessPolicy
from rest_access_policy.access_policy import AnonymousUser


class ReservationPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "search"],
            "principal": ["admin", "staff", "group:organization", "group:staff", "group:client"],
            "effect": "allow",
        },
        {
            "action": ["retrieve"],
            "principal": ["admin", "staff", "group:organization", "group:staff", "group:client"],
            "effect": "allow",
            "condition_expression": ["(is_owner:user or is_owner:approved_by or is_owner:organization)"]
        },
        # {
        #     "action": ["retrieve"],
        #     "principal": ["group:client"],
        #     "effect": "allow",
        #     "condition": "is_owner:guest"
        # },
        {
            "action": ["destroy", "update", "partial_update"],
            "principal": ["admin", "staff", "group:organization", "group:staff", "group:client"],
            "effect": "allow",
            "condition_expression": ["(is_owner:user or is_owner:approved_by or is_owner:organization)"]
        },
        {
            "action": ["create"],
            "principal": ["*"],
            "effect": "allow",
        },
    ]

    def is_owner(self, request, view, action, field: str) -> bool:
        reservation = view.get_object()
        print(f'client is {reservation.user}, user is {request.user}')
        user = request.user or AnonymousUser()
        if user.is_superuser or user.is_staff:
            return True
        if field == "organization":
            return reservation.organization.owner == user
        return getattr(reservation, field) == user


