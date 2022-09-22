from rest_framework import serializers
from .models import AllTransaction, OtherPayment, Transaction

class KhaltiVerifySerializer(serializers.ModelSerializer):
    model=Transaction
    fields = (
        'initiator',
        'paid_amount',
        'payment_token'
    )

class OtherPaymentSerializer(serializers.ModelSerializer):
    model = OtherPayment
    fields = (
        'initiator',
        'amount',
        'remarks'
    )


class AllTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllTransaction
        fields = '__all__'