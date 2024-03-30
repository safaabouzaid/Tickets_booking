from rest_framework import serializers
from .models import Booking,Companion

class FlightBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        #fields = ['id', 'user', 'flight_id', 'booking_date', 'seat_class', 'status']




class CompanionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companion
        fields = '__all__'



