from rest_framework import serializers
from .models import Booking,Passenger

class FlightBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        #fields = ['id', 'user', 'flight_id', 'booking_date', 'seat_class', 'status']
    def create(self, validated_data):
        passengers_data = validated_data.pop('passengers', [])
        booking = Booking.objects.create(**validated_data)
        for passenger_data in passengers_data:
            Passenger.objects.create(booking=booking, **passenger_data)
        return booking

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = '__all__'



