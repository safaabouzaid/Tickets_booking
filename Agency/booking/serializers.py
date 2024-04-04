from rest_framework import serializers
from .models import Booking,Passenger,Baggage
from flights.models import Flight#,FlightSeatClass


class BaggageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Baggage
        fields = '__all__'

class PassengerSerializer(serializers.ModelSerializer):
    baggages = BaggageSerializer(many=True, read_only=True)

    class Meta:
        model = Passenger
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields =['user','Passenger','outbound_flight','return_flight','trip_type']


    '''
    def validate(self, data):
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
    # if not outbound_flight.flightseatclass_set.filter(id=seat_class_id).exists():
     #       raise serializers.ValidationError("Selected seat class is not available for the outbound flight")

     return data
    '''

    def create(self, validated_data):
        passengers_data = validated_data.pop('passengers', [])
        booking = Booking.objects.create(**validated_data)
        for passenger_data in passengers_data:
            Passenger.objects.create(booking=booking, **passenger_data)
        return booking







