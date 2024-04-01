from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Booking,Passenger
from rest_framework.response import Response
from .serializers import FlightBookingSerializer,PassengerSerializer,PassengerSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

# Create your views here.

class BookingView(APIView):

    def post(self, request):
        serializer = FlightBookingSerializer(data=request.data)
        if serializer.is_valid():
            # Assign current user to booking
            serializer.validated_data['user'] = request.user

            # Check if it's a round trip booking
            trip_type = serializer.validated_data.get('trip_type')
            if trip_type == 'RT':
                # If it's a round trip, make sure both outbound and return flights are provided
                outbound_flight = serializer.validated_data.get('outbound_flight')
                return_flight = serializer.validated_data.get('return_flight')
                if not outbound_flight or not return_flight:
                    return Response({"error": "Both outbound and return flights are required for round trip booking"},
                                    status=status.HTTP_400_BAD_REQUEST)

            # Save the booking
            booking = serializer.save()

            # Check if companions are provided in the request data
            passengers_data = request.data.get('passengers', [])
            
            # Validate passengers
            try:
                self.validate_passengers(passengers_data, booking)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            for passenger_data in passengers_data:
                # Check if the passenger already exists in the booking
                passport_number = passenger_data.get('passport_number')
                if booking.passengers.filter(passport_number=passport_number).exists():
                    return Response({"error": f"Passenger with passport number {passport_number} is already booked in this flight"},
                                    status=status.HTTP_400_BAD_REQUEST)

                # Check if the passenger already exists in the database
                if Passenger.objects.filter(passport_number=passport_number).exists():
                    return Response({"error": f"Passenger with passport number {passport_number} already exists"},
                                    status=status.HTTP_400_BAD_REQUEST)

                passenger_serializer = PassengerSerializer(data=passenger_data)
                if passenger_serializer.is_valid():
                    passenger_serializer.save(booking=booking)
                else:
                    return Response(passenger_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def validate_passengers(self, passengers_data, booking):
        # Additional validation logic can be added here if needed
        for passenger_data in passengers_data:
            passport_number = passenger_data.get('passport_number')
            if booking.passengers.filter(passport_number=passport_number).exists():
                raise ValidationError(f"Passenger with passport number {passport_number} is already booked in this flight")


'''
class BookingView(APIView):
    def post(self, request):
        serializer = FlightBookingSerializer(data=request.data)
        if serializer.is_valid():
            # Assign current user to booking
            serializer.validated_data['user'] = request.user

            # Check if it's a round trip booking
            trip_type = serializer.validated_data.get('trip_type')
            if trip_type == 'RT':
                # If it's a round trip, make sure both outbound and return flights are provided
                outbound_flight = serializer.validated_data.get('outbound_flight')
                return_flight = serializer.validated_data.get('return_flight')
                if not outbound_flight or not return_flight:
                    return Response({"error": "Both outbound and return flights are required for round trip booking"},
                                    status=status.HTTP_400_BAD_REQUEST)

            # Save the booking
            booking = serializer.save()

            # Check if companions are provided in the request data
            passengers_data = request.data.get('passengers', [])
            for passenger_data in passengers_data:
                passenger_serializer = PassengerSerializer(data=passenger_data)
                if passenger_serializer.is_valid():
                    passenger_serializer.save(booking=booking)
                else:
                    return Response(passenger_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    #new

    def validate_passengers(self, passengers_data):
        passenger_ids = [passenger_data.get('passport_number') for passenger_data in passengers_data]
        if len(passenger_ids) != len(set(passenger_ids)):
            raise ValidationError("Passenger with the same passport number cannot book the same flight multiple times")

        #else:
         #return Response({"message": "Booking successful"})

'''
'''
    def post(self, request):
        ...

        # Check if companions are provided in the request data
        passengers_data = request.data.get('passengers', [])
        self.validate_passengers(passengers_data)

        ...
'''



class PassengerViewSet(viewsets.ModelViewSet):
    queryset = Passenger.objects.prefetch_related('baggages')
    serializer_class = PassengerSerializer
