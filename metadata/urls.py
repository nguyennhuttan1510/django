from rest_framework.routers import DefaultRouter

from metadata.views import MetadataView

router = DefaultRouter()
router.register(r'metadata', MetadataView, basename='metadata')
urlpatterns = router.urls