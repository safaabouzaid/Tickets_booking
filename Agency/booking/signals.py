
'''
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from .models import Booking

@receiver(post_save, sender=Booking)
def send_booking_reminder(sender, instance, created, **kwargs):
    if created:  # يتم إرسال الإشعار فقط عند إنشاء الحجز
        outbound_flight_date = instance.outbound_flight.departure_date

        # تاريخ ووقت الإشعار (24 ساعة قبل موعد اقلاع الرحلة)
        reminder_datetime = outbound_flight_date - timedelta(hours=24)

        # إذا كان تاريخ ووقت الإشعار قد حان، فأرسل الإشعار
        if timezone.now() >= reminder_datetime:
            notify.send(instance.user, 
                        verb=f"Your flight is coming up on {outbound_flight_date}. Don't forget to prepare!")


'''
