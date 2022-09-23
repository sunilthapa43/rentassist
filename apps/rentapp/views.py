from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rentassist.utils.views import AuthByTokenMixin
from users.models import Owner
from django.db.models import Sum
from .models import Complaint, Rent, Room
from rest_framework import viewsets
from .serializers import  ComplaintCreationSerializer, ComplaintSerializer, ComplaintSerializerAdmin, CreateRoomSerializer, RentSerializer, RoomSerializer
from rentassist.utils.response import exception_response, prepare_response
     
class RentViewSet(AuthByTokenMixin, viewsets.ModelViewSet):
    serializer_class = RentSerializer
    queryset = Rent.objects.all()
    def list(self, request, *args, **kwargs):
        queryset = Rent.objects.filter(tenant__owner__owner = request.user.id) 
        serializer = RentSerializer(queryset, many=True)
        if request.user.is_owner:
            return Response(serializer.data)    
        
        if not request.user.is_owner:
            queryset = Rent.objects.filter(tenant__tenant__tenant=request.user.tenant)
            serializer = RentSerializer(queryset, many=True)
            return Response(serializer.data)
    

class DueRentView(AuthByTokenMixin, GenericAPIView):
    def get(self, request, *args, **kwargs):
        queryset = Rent.objects.filter(tenant__owner__owner = request.user.id)
        print(queryset)
        due_amount = queryset.aggregate(Sum('due_amount'))
        due_amount = 5000
        return Response(due_amount)

class ComplaintViewSet(AuthByTokenMixin, viewsets.ModelViewSet):
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
        serializer =  ComplaintCreationSerializer(data=request.data ) 
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
    
    
    # def update(self, request, pk=None, *args, **kwargs):
    #     queryset = Complaint.objects.filter(tenant__owner = request.user.id)
    #     obj = get_object_or_404(queryset, pk=pk)
        
    #     if not obj:
    #         response = prepare_response(
    #                  success=False,
    #                  message='Does not exist'
    #              )
    #         return Response(response)  
    #     serializer =  ComplaintSerializer(obj) 
    #     serializer.save()

class RoomViewSet(AuthByTokenMixin, viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def create(self, request, *args, **kwargs):
        owner = request.user
        o = Owner.objects.get(owner = owner)
        print(o)
        print(type(o))
        serializer = CreateRoomSerializer(data=request.data)
        if serializer.is_valid():
            image=serializer.validated_data['image']
            price = serializer.validated_data['price']
            internet_price = serializer.validated_data['internet_price']
            water_usage_price = serializer.validated_data['water_usage_price']
            nagarpalika_fohr_price = serializer.validated_data['nagarpalika_fohr_price']
            electricity_rate = serializer.validated_data['electricity_rate']
            try:
                obj = Room.objects.create(
                    owner=o,
                    image=image,
                    price=price,
                    internet_price=internet_price,
                    water_usage_price=water_usage_price,
                    nagarpalika_fohr_price=nagarpalika_fohr_price,
                    electricity_rate = electricity_rate
                )
                obj.save()
                response = prepare_response(
                    success=True,
                    message='successfully added dummy agreement on room',
                    data = serializer.data,
                    meta={
                        "id":obj.id
                    }
                )
                return Response(response)
            
            except Exception as e:
                return exception_response(e, serializer)
        
        else:
            response = prepare_response(
                success=False,
                message='Invalid request',
                data=serializer.data
            )
            return Response(response)