from urllib import response
from xml.etree.ElementPath import prepare_star
from rest_framework.response import Response

from rentassist.utils.views import AuthByTokenMixin
from .models import Complaint, Rent, Room
from rest_framework import viewsets
from .serializers import  ComplaintSerializer, ComplaintSerializerAdmin, RentSerializer, RoomSerializer
from rentassist.utils.response import exception_response, prepare_response
     
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
            queryset = Complaint.objects.filter(tenant__owner__owner = request.user.id)
            serializer=ComplaintSerializerAdmin(queryset, many=True)
            response = prepare_response(
                success=True,
                message = 'complaints fetched successfully',
                data= serializer.data
            )
            return Response(response)
    
    def create(self, request, *args, **kwargs):
        
        if request.user.is_owner:
            response = prepare_response(
                success=False,
                message = 'You are not allowed to complain'
            )
            return Response(response)
        serializer =  ComplaintSerializer(data=request.data ) 
        if serializer.is_valid():
            try:
                tenant = request.user.tenant
                
                image = request.data['image']
                title=serializer.validated_data['title']
                description=serializer.validated_data['description']
                # status = serializer.validated_data['status']
                urgency_level=serializer.validated_data['urgency_level']
                
                obj = Complaint.objects.create(
                    tenant=tenant,
                    image=image,
                    title=title,
                    description=description,
                    urgency_level=urgency_level)
                obj.save()
                response = prepare_response(
                    success=True,
                    message='Complaint added successfully',
                    data=serializer.data
                )
                return Response(response)
            except Exception as e:
                return exception_response(e, serializer)
        else:
            response = prepare_response(
                success=False,
                message="Invalid request",
                data=serializer.data
            )
            return Response(response)

class RoomViewSet(AuthByTokenMixin, viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer