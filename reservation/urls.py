from rest_framework.routers import DefaultRouter

from reservation.views import ReservationViewSet

router = DefaultRouter()
router.register(r'reservations', ReservationViewSet, basename='reservation')
urlpatterns = router.urls