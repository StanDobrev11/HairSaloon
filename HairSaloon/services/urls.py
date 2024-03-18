from django.urls import path

from HairSaloon.services.views import DetailServiceView

urlpatterns = [
    path('<int:pk>', DetailServiceView.as_view(), name='detail service')
]
