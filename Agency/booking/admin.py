from django.contrib import admin
from . models import Booking,Passenger,Baggage

# Register your models here.
admin.site.register(Booking)
admin.site.register(Passenger)
admin.site.register(Baggage)

