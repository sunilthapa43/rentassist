from .models import ElectricityUnit, Ocr
from rest_framework import serializers  


class ElectricityUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricityUnit
        fields = (
            'tenant',
            'current_reading'
        )

class RunOcrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ocr
        fields = ('image',)

    