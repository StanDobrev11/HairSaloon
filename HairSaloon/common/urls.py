from django.urls import path

from HairSaloon.common.views import IndexView, ListBlogView, AboutView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('blog/', ListBlogView.as_view(), name='blog'),
    path('about/', AboutView.as_view(), name='about'),
]
