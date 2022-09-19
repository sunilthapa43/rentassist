from rest_framework.response import Response

from rentassist.utils.views import AuthByTokenMixin
from .models import Complaint, Rent#, Room
from rest_framework import viewsets
from .serializers import  ComplaintSerializer, RentSerializer#, RoomSerializer
from rentassist.utils.response import prepare_response
     
class RentViewSet(AuthByTokenMixin, viewsets.ModelViewSet):
    serializer_class = RentSerializer
    queryset = Rent.objects.all()
    def list(self, request, *args, **kwargs):
        queryset = Rent.objects.filter(tenant__owner = request.user.id) 
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
            print(request.user.id)
            queryset = Complaint.objects.filter(tenant__owner = request.user.id)
            serializer=ComplaintSerializer(queryset, many=True)
            response = prepare_response(
                success=True,
                message = 'complaints fetched successfully',
                data= serializer.data
            )
            return Response(response)



# class RoomViewSet(AuthByTokenMixin, viewsets.ModelViewSet):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer