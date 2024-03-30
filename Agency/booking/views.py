from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Booking
from rest_framework.response import Response
from .serializers import FlightBookingSerializer,CompanionSerializer
# Create your views here.
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

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



'''


from rest_framework.response import Response
from rest_framework import status

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
            companions_data = request.data.get('companions', [])
            for companion_data in companions_data:
                companion_serializer = CompanionSerializer(data=companion_data)
                if companion_serializer.is_valid():
                    companion_serializer.save(booking=booking)
                else:
                    return Response(companion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
