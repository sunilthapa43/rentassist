from pyexpat import model
from rest_framework.serializers import ModelSerializer
from .models import Agreement, Document

class DocumentSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"


class AgreementSerializer(ModelSerializer):
    class Meta:
        model = Agreement
        fields = (
            'price',
            'tenant',
            'internet_price',
            'water_usage_price',
            'nagarpalika_fohr_price',
            'electricity_rate',
        )