from django.urls import path, include

from HairSaloon.accounts.views import LoginUserView, RegisterUserView, logout_view, HairSalonEditUserView, \
    HairSalonPasswordChangeView

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),

    path(
        'profile/<int:pk>/',
        include([
            path('', HairSalonEditUserView.as_view(), name='edit user'),
            path('passchange/', HairSalonPasswordChangeView.as_view(), name='password change')
        ])
    )
]
