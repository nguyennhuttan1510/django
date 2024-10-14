from rest_framework.routers import DefaultRouter

from reservation.views import ReservationViewSet

router = DefaultRouter()
router.register(r'booking', ReservationViewSet, basename='booking')
urlpatterns = router.urls