from rest_framework.response import Response

from rentassist.utils.views import AuthByTokenMixin
from .models import Complaint, Rent
from rest_framework import viewsets
from .serializers import  ComplaintSerializer, RentSerializer
from rentassist.utils.response import prepare_response
     
class RentViewSet(AuthByTokenMixin, viewsets.ModelViewSet):
    
    def list(self, request, *args, **kwargs):
        queryset = Rent.objects.all() 
        serializer = RentSerializer(queryset, many=True)
        if request.user.is_owner:
            return Response(serializer.data)    
        
        if not request.user.is_owner:
            queryset = Rent.objects.filter(tenant=request.user.tenant)
            serializer = RentSerializer(queryset, many=True)
            return Response(serializer.data)

class CompalaintViewSet(AuthByTokenMixin, viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer

    def list(self, request, *args, **kwargs):
        if not request.user.is_owner:
            queryset = Complaint.objects.filter(tenant = request.user.tenant)
            serializer = ComplaintSerializer(queryset, many=True)
            response = prepare_response(
                success=True,
                messgae='your complaints are fetched',
                data=serializer.data
            )
            return Response(response)
        else:
            #todo
            queryset = Complaint.objects.filter()
            serializer=ComplaintSerializer(queryset, many=True)



