from django.urls import path
from .import views

from .views import index


urlpatterns = [
    path('', views.home, name='home'),
    path('trips/', views.list_trips, name='list_trips'),
    path('trips/<int:trip_id>/', views.show_trip, name='show_trip'),
    path('bookings/', views.listBookings, name='list_bookings'),
    path('bookings/add/', views.add, name='add'),
    path('bookings/add/<int:trip_id>/', views.add_booking, name='add_booking'),
    path('bookings/<int:booking_id>/', views.show_booking, name='show_booking'),
    path('bookings/<int:booking_id>/edit/', views.edit, name='edit_booking'),
    path('bookings/<int:booking_id>/remove/', views.remove, name='remove_booking'),
    path('trips/<int:trip_id>/book/', views.book_trip, name='book_trip'),
    path('notifications/', views.notifications, name='notifications'),
]

