from django.urls import path, include

from HairSaloon.accounts.views import LoginUserView, RegisterUserView, logout_view, ProfileUserView

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),

    path(
        'profile/<int:pk>/',
        include([
            path('', ProfileUserView.as_view(), name='profile'),
        ])
    )
]
