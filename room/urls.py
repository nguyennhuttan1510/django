from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from room import views
from room.views import RoomViewSet

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='room')
urlpatterns = router.urls