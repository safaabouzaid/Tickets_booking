from django.urls import path, include
from rest_framework.routers import DefaultRouter
#from .views import BookingView
from . import views

urlpatterns = [
#path('bookings/', BookingView.as_view(), name='create_booking'),
#path('bookings/', views.Bookingview, name='create_booking'),
path('bookings/', views.create_booking, name='create_booking'),

]
