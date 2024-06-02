from rest_framework.routers import DefaultRouter

from asset.views import AssetViewSet

router = DefaultRouter()
router.register(r'assets', AssetViewSet, basename='assets')
urlpatterns = router.urls