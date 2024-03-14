from django.urls import path
from organization import views
urlpatterns = [
    path('', views.view_organization, name='view_organizations'),
    path('<int:pk>', views.view_organization, name='view_organizations'),
]