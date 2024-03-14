from django.urls import path

from convenience import views

urlpatterns = [
    path('', views.view_conveniences, name='view_conveniences'),
    path('<int:pk>', views.view_conveniences, name='view_convenience'),
]