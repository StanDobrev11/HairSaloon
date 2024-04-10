from django.urls import path, include

from HairSaloon.common.views import IndexView, ListBlogView, AboutView, AddCommentView, DeleteCommentView, \
    ApproveCommentView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),

    path(
        'blog/',
        include([
            path('', ListBlogView.as_view(), name='blog'),
            path('add/', AddCommentView.as_view(), name='add comment'),
            path('<int:pk>/delete/', DeleteCommentView.as_view(), name='delete comment'),
            path('<int:pk>/approve/', ApproveCommentView.as_view(), name='approve comment'),
        ])
    )
]
