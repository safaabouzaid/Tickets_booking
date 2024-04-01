from rest_framework import serializers
from .models import Booking,Passenger,Baggage

class FlightBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        #sedra

    def validate(self, data):
     print("Validating data...")
     outbound_flight = data.get('outbound_flight')
     return_flight = data.get('return_flight')

     if outbound_flight == return_flight:
        raise serializers.ValidationError("Outbound and return flights cannot be the same")

     passengers_data = data.get('passengers', [])
     passenger_names = [passenger.get('name') for passenger in passengers_data]
     if len(passenger_names) != len(set(passenger_names)):
        raise serializers.ValidationError("Passenger names must be unique within a booking")

     passport_numbers = [passenger.get('passport_number') for passenger in passengers_data]
     if len(passport_numbers) != len(set(passport_numbers)):
        raise serializers.ValidationError("Passport numbers must be unique within a booking")

     return data


    def create(self, validated_data):
        passengers_data = validated_data.pop('passengers', [])
        booking = Booking.objects.create(**validated_data)
        for passenger_data in passengers_data:
            Passenger.objects.create(booking=booking, **passenger_data)
        return booking




class BaggageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Baggage
        fields = '__all__'


class PassengerSerializer(serializers.ModelSerializer):
    baggages = BaggageSerializer(many=True, read_only=True)

    class Meta:
        model = Passenger
       # fields = '__all__'
        fields=['first_name','last_name','date_of_birth','gender','passport_number','phone_number','baggages']





