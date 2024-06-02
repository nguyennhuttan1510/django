from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from service import views
from service.views import RoomViewSet

router = DefaultRouter()
router.register(r'services', RoomViewSet, basename='services')
urlpatterns = router.urls