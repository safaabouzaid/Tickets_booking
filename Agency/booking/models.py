from django.db import models
from operator import mod
from account.models import User
from django.dispatch import receiver
from django.utils import timezone
from django.utils.timezone import now
from django.db.models.signals import post_save
from datetime import datetime, timedelta 
from account.models import User
from datetime import timedelta

from flights.models import Flight#,FlightSeatClass

# Create your models here.


class Passenger(models.Model):
    GENDER_CHOICES = (
        ('Mr','Mr'),
        ('Ms','Ms'),
        ('Mrs','Mrs'),
       )
      
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=3, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    passport_number = models.CharField(max_length=100)
    def __str__(self):
             return f"{self.first_name} {self.last_name}"


    def add_baggage(self, baggage_type):
        Baggage.objects.create(passenger=self, baggage_type=baggage_type)

    def has_baggage(self, baggage_type):
        return self.baggages.filter(baggage_type=baggage_type).exists()

class Baggage(models.Model):
    BAGGAGE_CHOICES = (
        ('HI', 'Hand Item'),
        ('PI', 'Personal Item'),
        ('CB', 'Checked Baggage'),
    )
    
    passenger = models.ForeignKey(Passenger, related_name='baggages', on_delete=models.CASCADE)
    baggage_type = models.CharField(max_length=2, choices=BAGGAGE_CHOICES,default='HI')  # اختيار نوع الحقيبة

    def __str__(self):
        return f"{self.passenger.first_name} {self.passenger.last_name}'s {self.get_baggage_type_display()}"

class Booking(models.Model):
    STATUS_CHOICES = (
        ('CNL', 'Canceled'),
        ('PPD', 'Postponed'),
        ('CMP', 'Completed'),
    
    )
    TRIP_TYPE_CHOICES = (
        ('OW', 'One Way'),
        ('RT', 'Round Trip'),
    )

    booking_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    Passenger= models.ForeignKey(Passenger, on_delete=models.SET_NULL,null=True)
    outbound_flight = models.ForeignKey(Flight, related_name='outbound_bookings', on_delete=models.SET_NULL, null=True)
    return_flight = models.ForeignKey(Flight, related_name='return_bookings', on_delete=models.SET_NULL, null=True, blank=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    trip_type = models.CharField(max_length=10, choices=TRIP_TYPE_CHOICES, default='OW')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='PPD')
    
    
    
    def update_flight_available_seats(self):
        # احتساب عدد المقاعد المحجوزة على الرحلة
        outbound_flight = self.outbound_flight
        booked_seats = Booking.objects.filter(outbound_flight=outbound_flight).count()
        
        # حساب عدد المقاعد المتاحة بعد الحجز
        available_economy_seats = max(0, outbound_flight.airplane.seattype.economy_capacity - booked_seats)
        available_business_seats = max(0, outbound_flight.airplane.seattype.business_class_capacity - booked_seats)
        available_first_class_seats = max(0, outbound_flight.airplane.seattype.first_class_capacity - booked_seats)
        
        # تحديث عدد المقاعد المتاحة على الرحلة
        outbound_flight.available_economy_seats = available_economy_seats
        outbound_flight.available_business_seats = available_business_seats
        outbound_flight.available_first_class_seats = available_first_class_seats
        outbound_flight.save()
        
        return {
            'economy': available_economy_seats,
            'business': available_business_seats,
            'first_class': available_first_class_seats}

'''
    @receiver(post_save, sender=Booking)
    def update_flight_seats(sender, instance, **kwargs):
     if instance.outbound_flight:
        instance.outbound_flight.update_available_seats()
        instance.outbound_flight.save()


'''
class PushNotificationToken(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE) #we are not using a real User model in this article. You can use the User model specified in your application.
    fcm_token = models.CharField(max_length=200, unique=True)




