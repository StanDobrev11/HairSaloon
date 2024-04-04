from django.urls import path, include

from HairSaloon.services.views import DetailServiceView, CreateServiceView, ListServiceView, DeleteServiceView, \
    EditServiceView

urlpatterns = [
    path('', ListServiceView.as_view(), name='list_services'),
    path('create/', CreateServiceView.as_view(), name='create_service'),

    path(
        '<int:pk>/',
        include([
            path('', DetailServiceView.as_view(), name='detail service'),
            path('delete/', DeleteServiceView.as_view(), name='delete service'),
            path('edit/', EditServiceView.as_view(), name='edit service'),
        ])
    ),
]
