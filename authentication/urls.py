from rest_framework.routers import DefaultRouter
from authentication.views import UserViewSet

router = DefaultRouter()
router.register(r'authentications', UserViewSet, basename='authentication')
urlpatterns = router.urls