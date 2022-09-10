from rest_framework import serializers

from .models import   Complaint, Deposit, Rent




class RentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = "__all__"


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = "__all__"



class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = "__all__"


