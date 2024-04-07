from django.test import TestCase,Client
from account.models import User
from datetime import datetime, timedelta
from .models import Airplane, SeatType,Policy,Airline,Flight, Airport


#class BasicTest(TestCase):
#   def test_1(self):
#      self.assertTrue(1==1)


class TestModels(TestCase):
    def test_model_airplane(self): 
        seats = SeatType.objects.create(economy=2, business_class=3, first_class=4)
        airplane = Airplane.objects.create(
            airplane_name='Test Item',
            manufacturer='ds',
            manufacturing_date='2003-02-10',
            seats=seats
        )
        self.assertEqual(str(airplane), 'Test Item')
        self.assertIsInstance(airplane, Airplane)



class TestFlightModel(TestCase):
    def setUp(self):
        # إعداد البيانات اللازمة للاختبار
        self.seat_type = SeatType.objects.create(economy=100, business_class=50, first_class=20)
        self.policy = Policy.objects.create(refundable=True, exchangeable=True, exchangeable_condition="Test condition", cancellation_period=timedelta(days=1))  # إنشاء كائن Policy
        self.airline = Airline.objects.create(
            airline_name='Test Airline',
            description='Test Description',
            policy=self.policy  # تحديد قيمة policy

        )
        self.airplane = Airplane.objects.create(
            airplane_name='Test Airplane',
            manufacturer='Test Manufacturer',
            manufacturing_date=datetime.now().date(),
            seats=self.seat_type
        )
        self.departure_airport = Airport.objects.create(
            airport_name='Departure Airport',
            IATA_code='DEP',
            contact_info='Contact Info',
            country='Country'
        )
        self.destination_airport = Airport.objects.create(
            airport_name='Destination Airport',
            IATA_code='DES',
            contact_info='Contact Info',
            country='Country'
        )

    def test_flight_model(self):
        # إنشاء كائن الرحلة
        flight = Flight.objects.create(
            airline=self.airline,
            airplane=self.airplane,
            airportDeparture=self.departure_airport,
            airportArrival=self.destination_airport,
            departure_date=datetime.now().date(),
            return_date=(datetime.now() + timedelta(days=1)).date(),
            duration=timedelta(hours=2),
            notes='Test Notes',
            ratings=4,
        )

        # التحقق من صحة البيانات المخزنة
        self.assertEqual(flight.airline.airline_name, 'Test Airline')
        self.assertEqual(flight.airplane.airplane_name, 'Test Airplane')
        self.assertEqual(flight.airportDeparture.airport_name, 'Departure Airport')
        self.assertEqual(flight.airportArrival.airport_name, 'Destination Airport')
        self.assertEqual(flight.departure_date, datetime.now().date())
        self.assertEqual(flight.return_date, (datetime.now() + timedelta(days=1)).date())
        self.assertEqual(flight.duration, timedelta(hours=2))
        self.assertEqual(flight.notes, 'Test Notes')
        self.assertEqual(flight.ratings, 4)
