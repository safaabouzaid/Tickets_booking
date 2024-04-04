from django.contrib import admin
from .models import Flight,Airline,Policy,SeatType,FlightSchedule,RefundedPayment,Airport,Airplane
# Register your models here.

admin.site.register(Flight)
admin.site.register(Airline)
admin.site.register(Policy)
admin.site.register(SeatType)
admin.site.register(RefundedPayment)
admin.site.register(FlightSchedule)
admin.site.register(Airport)
admin.site.register(Airplane)





