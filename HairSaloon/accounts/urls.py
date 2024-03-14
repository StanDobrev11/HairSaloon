from django.urls import path

from HairSaloon.accounts.views import LoginUserView

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login')
]
