from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer

from users.models import Profile


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['id'] = user.pk
        token['profile_id'] = Profile.objects.get(owner=user.pk).id
        return token
