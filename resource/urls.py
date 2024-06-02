from rest_framework.routers import DefaultRouter

from resource.views import ResourceViewSet

from django.urls import path
from django.contrib import admin
from resource.views import ResourceViewSet

# router = DefaultRouter()
# router.register(r'resources', ResourceViewSet, basename='resource')
# urlpatterns = router.urls

urlpatterns = [
    path('resources/', ResourceViewSet.as_view(), name='file-upload'),
]