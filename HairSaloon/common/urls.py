from django.urls import path, include
from django.views.generic import DetailView

from HairSaloon.common.views import IndexView, ListBlogView, AboutView, AddCommentView, DeleteCommentView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),

    path(
        'blog/',
        include([
            path('', ListBlogView.as_view(), name='blog'),
            path('add/', AddCommentView.as_view(), name='add comment'),
            path('<int:pk>/', DeleteCommentView.as_view(), name='delete comment'),
        ])
    )
]
