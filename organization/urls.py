from django.urls import path
from rest_framework import routers

from organization.views import OrganizationViewSet

router = routers.DefaultRouter()
router.register(r'organizations', OrganizationViewSet, basename='organizations')
urlpatterns = router.urls