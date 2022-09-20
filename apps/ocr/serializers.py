from .models import ElectricityUnit
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers  


class ElectricityUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricityUnit
        fields = (
            'image',
            'tenant'
        )

class ConfigBatti(serializers.ModelSerializer):
    class Meta:
        model = ElectricityUnit
        fields = ('tenant', 'image', 'current_reading')