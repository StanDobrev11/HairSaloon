from django.urls import path, include

from HairSaloon.services.views import DetailServiceView, CreateServiceView, ListServiceView, \
    ServiceToHairdresserAssociationView

urlpatterns = [
    path('', ListServiceView.as_view(), name='list_services'),
    path('create/', CreateServiceView.as_view(), name='create_service'),
    path('create/assign-hairdresser/', ServiceToHairdresserAssociationView.as_view(), name='assign_hairdresser'),

    path(
        '<int:pk>/',
        include([
            path('', DetailServiceView.as_view(), name='detail service'),
        ])
    ),
]
