from django.urls import path, include

from HairSaloon.bookings.views import BookingView, BookingDetailView, BookingDeleteView

urlpatterns = [
    path('', BookingView.as_view(), name='dashboard'),
    path(
        '<int:pk>/',
        include([
            path('deltails/', BookingDetailView.as_view(), name='booking details'),
            path('delete/', BookingDeleteView.as_view(), name='booking delete'),

        ])
    )
]
