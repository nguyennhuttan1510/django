from rest_framework.routers import DefaultRouter

from evaluation.views import EvaluationViewSet
from reservation.views import ReservationViewSet

router = DefaultRouter()
router.register(r'evaluations', EvaluationViewSet, basename='evaluation')
urlpatterns = router.urls