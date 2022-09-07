from .models import  Tenant,Complaint, Notification, Rent
from rest_framework import viewsets
from .serializers import  ComplaintSerializer,  NotificationSerializer,  RentSerializer,  TenantSerializer 
# Create your views here.


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
     
class RentViewSet(viewsets.ModelViewSet):
    queryset = Rent.objects.all()
    serializer_class = RentSerializer       

class CompalaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

