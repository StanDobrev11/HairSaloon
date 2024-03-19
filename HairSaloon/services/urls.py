from django.urls import path

from HairSaloon.services.views import DetailServiceView, get_service_duration

urlpatterns = [
    path('<int:pk>/', DetailServiceView.as_view(), name='detail service'),
    path('api/get-service-duration/<int:pk>/', get_service_duration, name='service duration'),
]
