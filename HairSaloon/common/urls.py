from django.urls import path

from HairSaloon.common.views import IndexView, BlogView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('blog/', BlogView.as_view(), name='blog'),
]
