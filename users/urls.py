from rest_framework.routers import DefaultRouter

from users.views import ProfileViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
urlpatterns = router.urls
