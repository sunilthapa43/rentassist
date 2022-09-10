from rest_framework import serializers
from .models import Transaction

class KhaltiVerifySerializer(serializers.ModelSerializer):
    model=Transaction
    fields = (
        'initiator',
        'paid_amount',
        'payment_token'
    )