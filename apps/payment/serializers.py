from rest_framework import serializers
from .models import AllTransaction, OtherPayment, Transaction

class KhaltiVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model=Transaction
        fields = (
            'paid_amount',
            'payment_token'
        )

class OtherPaymentSerializer(serializers.ModelSerializer):
    class Meta:
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