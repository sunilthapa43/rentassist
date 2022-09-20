from rest_framework import serializers

from .models import   Complaint, Rent, Room

class RentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = "__all__"



class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        exclude =('tenant',)

class ComplaintCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        exclude = ('tenant', 'date', 'is_solved')
    

class ComplaintSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'



class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model=Room
        fields =  '__all__'