from django.urls import path

from HairSaloon.common.views import IndexView, BlogView, AboutView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('about/', AboutView.as_view(), name='about'),
]
