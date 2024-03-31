from django.db import models
from operator import mod
from account.models import User
from datetime import datetime, timedelta 
from account.models import User
from flights.models import Flight,FlightSeatClass
# Create your models here.

class Booking(models.Model):
    TRIP_TYPE_CHOICES = (
        ('OW', 'One Way'),
        ('RT', 'Round Trip'),
    )
    STATUS_CHOICES = (
        ('CNL', 'Canceled'),
        ('PPD', 'Postponed'),
        ('CMP', 'Completed'),
    )
    booking_id= models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    outbound_flight = models.ForeignKey(Flight, related_name='outbound_bookings', on_delete=models.SET_NULL, null=True)
    return_flight = models.ForeignKey(Flight, related_name='return_bookings', on_delete=models.SET_NULL, null=True, blank=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    seat_class = models.ForeignKey(FlightSeatClass, on_delete=models.CASCADE)
    trip_type = models.CharField(max_length=2, choices=TRIP_TYPE_CHOICES, default='OW')
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='CMP')
    has_companions = models.BooleanField(default=False)
    #passengers = models.ForeignKey(Passenger, related_name='bookings')
    def __str__(self):
        return f'Booking {self.booking_id} - User: {self.user.username} - Status: {self.get_status_display()}'



class Passenger(models.Model):
    GENDER_CHOICES = (
        ('Mr', 'Mr'),
        ('Ms', 'Ms'),
        ('Mrs', 'Mrs'),
    )    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    booking = models.ForeignKey(Booking, related_name='passengers', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=3, choices=GENDER_CHOICES)
    passport_number = models.CharField(max_length=20)
    phone_number=models.CharField(max_length=100,null=True,blank=True)
    def str(self):
             return f" {self.first_name} {self.last_name}"


