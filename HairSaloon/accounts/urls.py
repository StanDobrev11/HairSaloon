from django.urls import path

from HairSaloon.accounts.views import LoginUserView, RegisterUserView, LogoutUserView

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
]
