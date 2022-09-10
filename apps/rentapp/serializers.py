from rest_framework import serializers

from .models import   Complaint, Rent

class RentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = "__all__"



class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = "__all__"


