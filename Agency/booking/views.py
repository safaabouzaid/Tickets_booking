from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Booking,Passenger
from .serializers import BookingSerializer,PassengerSerializer,PassengerSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view ,permission_classes
from flights.models import Flight
# Create your views here.

@api_view(['POST'])
def create_booking(request):
    if request.method == 'POST':
        booking_data = request.data.get('booking', {})
        passenger_data = request.data.get('passenger', {})
        
        if not booking_data or not passenger_data:
            return Response({'message': 'Booking and Passenger data are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        outbound_flight_id = booking_data.get('outbound_flight')
        return_flight_id = booking_data.get('return_flight') 
        

        if outbound_flight_id == return_flight_id:
            return Response({'message': 'Outbound and return flights cannot be the same'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            outbound_flight = Flight.objects.get(id=outbound_flight_id)
            return_flight = Flight.objects.get(id=return_flight_id)
        except Flight.DoesNotExist:
            return Response({'message': 'One of the flights does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        passport_number = passenger_data.get('passport_number')
        matching_passengers = Passenger.objects.filter(passport_number=passport_number)
        
        if matching_passengers.exists():
            passenger = matching_passengers.first()
        else:
            passenger_serializer = PassengerSerializer(data=passenger_data)
            if passenger_serializer.is_valid():
                passenger = passenger_serializer.save()
            else:
                return Response(passenger_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        for booking in Booking.objects.filter(Passenger=passenger.id):
            if booking.outbound_flight_id == outbound_flight_id or (booking.return_flight_id and booking.return_flight_id == return_flight_id):
               return Response({'message': 'Passenger already booked on one of these flights'}, status=status.HTTP_400_BAD_REQUEST)
        booking_data['Passenger'] = passenger.id
        booking_serializer = BookingSerializer(data=booking_data)
        if booking_serializer.is_valid():
            booking = booking_serializer.save()
            return Response({'message': 'Booking created successfully', 'booking_id': booking.booking_id}, status=status.HTTP_201_CREATED)
        return Response(booking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
'''


@api_view(['POST'])
def Bookingview(request):
    if request.method == 'POST':
        # Retrieve flight data
        outbound_flight_id = request.data.get('outbound_flight')
        return_flight_id = request.data.get('return_flight')
        
        passport_number = request.data.get('passenger').get('passport_number')
        existing_passenger = Passenger.objects.filter(passport_number=passport_number).first()
        
        if existing_passenger: 
            booking_data = {
                'user': request.user.id,  
                'passengers': [existing_passenger.id],  # Change 'Passenger' to 'passengers'
                'outbound_flight_id': outbound_flight_id,
                'return_flight_id': return_flight_id,
                'trip_type': request.data.get('trip_type')
            }
            
            booking_serializer = BookingSerializer(data=booking_data)
            if booking_serializer.is_valid():
                booking = booking_serializer.save()
                return Response({"message": "Booking created successfully", "booking": booking_serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(booking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:  # If passenger doesn't exist, create passenger and booking
            passenger_serializer = PassengerSerializer(data=request.data.get('passenger'))
            if passenger_serializer.is_valid():
                passenger = passenger_serializer.save()
                
                # Create Booking object
                booking_data = {
                    'user': request.user.id,  # Assuming user is authenticated
                    'passengers': [passenger.id],  # Change 'Passenger' to 'passengers'
                    'outbound_flight_id': outbound_flight_id,
                    'return_flight_id': return_flight_id,
                    'trip_type': request.data.get('trip_type')
                }
                
                booking_serializer = BookingSerializer(data=booking_data)
                if booking_serializer.is_valid():
                    booking = booking_serializer.save()
                    return Response({"message": "Booking created successfully", "booking": booking_serializer.data}, status=status.HTTP_201_CREATED)
                else:
                    passenger.delete()
                    return Response(booking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(passenger_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
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
