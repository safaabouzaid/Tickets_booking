from rest_framework import serializers
from .models import Flight,Review,Airline
from rest_framework_simplejwt.tokens import AccessToken


class FlightSerializer(serializers.ModelSerializer) :
    
    
    airline = serializers.PrimaryKeyRelatedField(queryset=Airline.objects.all())  # Add this field
    class Meta:
        model=Flight
        fields="__all__"

    def get_reviews(self,obj):
        reviews=obj.reviews.all()
        serializer=ReviewSerializer(reviews,many=True)
        return serializer.data

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model=Review
        fields="__all__"

