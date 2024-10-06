"""
URL configuration for tutorial project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views

from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework_simplejwt.views import TokenVerifyView

from services.token.view import CustomTokenObtainPairView, CustomTokenVerifyView


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include(router.urls)),
                  path('api-auth/', include('rest_framework.urls')),
                  path("", include("quickstart.urls"), name="quickstart"),
                  path("", include("resource.urls"), name="resource"),
                  path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
                  path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
                  path('token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),

                  path("", include("users.urls"), name="users"),
                  path("", include("reservation.urls"), name="reservations"),
                  path("", include("service.urls"), name="services"),
                  path("", include("authentication.urls"), name="authentications"),
                  path("", include("organization.urls"), name="organizations"),
                  path("conveniences/", include("convenience.urls")),
                  # path("", include("asset.urls")),
                  path("", include("evaluation.urls")),
                  path("", include("metadata.urls")),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
