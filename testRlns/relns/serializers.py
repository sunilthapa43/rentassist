from rest_framework import serializers

from .models import Owner, Tenant, Chat


class OwnerSerializer(serializers.ModelSerializer):
    class Meta: 
        model= Owner
        fields= '__all__'


class TenantSerializer(serializers.ModelSerializer):
    class Meta: 
        model= Tenant
        fields= '__all__'


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model= Chat
        fields ='__all__'
        

