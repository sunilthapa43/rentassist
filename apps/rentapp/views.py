from .models import Complaint, Rent
from rest_framework import viewsets
from .serializers import  ComplaintSerializer, RentSerializer
# Create your views here.



     
class RentViewSet(viewsets.ModelViewSet):
    queryset = Rent.objects.all()
    serializer_class = RentSerializer       

class CompalaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer


