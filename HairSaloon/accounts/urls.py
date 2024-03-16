from django.urls import path

from HairSaloon.accounts.views import LoginUserView, RegisterUserView, logout_view

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
]
