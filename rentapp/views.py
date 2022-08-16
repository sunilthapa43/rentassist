from django.shortcuts import render
from .models import Owner, Tenant, OtherPayment, Agreement, Complaint, Deposit, Document, Electricity, Notification, Rent, Transaction 
from rest_framework import viewsets
from .serializers import AgreementSerializer, ComplaintSerializer, DepositSerializer, DocumentSerializer, ElectricitySerializer, NotificationSerializer, OtherPaymentSerializer, OwnerSerializer, RentSerializer, TransactionSerializer, TenantSerializer 
# Create your views here.

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    
class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
class TransactionViewSet(viewsets.ModelViewSet): 
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer     
class RentViewSet(viewsets.ModelViewSet):
    queryset = Rent.objects.all()
    serializer_class = RentSerializer       
class AgreementViewSet(viewsets.ModelViewSet):
    queryset = Agreement.objects.all()
    serializer_class = AgreementSerializer
class CompalaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
class DepositViewSet(viewsets.ModelViewSet):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer
class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
class ElectricityViewSet(viewsets.ModelViewSet):
    queryset = Electricity.objects.all()
    serializer_class = ElectricitySerializer
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
class OtherPaymentViewSet(viewsets.ModelViewSet):
    queryset = OtherPayment.objects.all()
    serializer_class = OtherPaymentSerializer

class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer