from .models import ElectricityUnit, Ocr
from rest_framework import serializers  
from rest_flex_fields import FlexFieldsModelSerializer

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


class ElectricityUnitSerializerA(FlexFieldsModelSerializer):
    class Meta:
        model = ElectricityUnit
        fields = '__all__'