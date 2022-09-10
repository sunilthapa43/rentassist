
from rest_framework.response import Response
from payment.models import Transaction

from rentassist.utils.views import AuthByTokenMixin
from .models import Document, Agreement
from rest_framework.viewsets import ModelViewSet
from .serializers import DocumentSerializer, AgreementSerializer


class AgreementViewSet(AuthByTokenMixin, ModelViewSet):
    
    serializer_class = AgreementSerializer
    def list(self, request, *args, **kwargs):
        user = request.user
        if user.is_owner:
            queryset = Agreement.objects.all()
            serializer = AgreementSerializer(queryset, many=True)
            response = {
                "success":True,
                "message":"Successfully fetched agreements",
                "data": serializer.data
            }
            return Response(response)
        
        
        try:
            tenant = request.user
            username = tenant.username
            agreement = Agreement.objects.get(tenant = tenant)
            if agreement:
                rent_price = agreement.price
                water_usage_price = agreement.water_usage_price
                electricity_rate = agreement.electricity_rate
                internet_price = agreement.internet_price
                created = agreement.created
                updated = agreement.updated
                deadline = agreement.deadline

                response = {
                    "success": True,
                    "message": "Your Agreement details fetched successfully",
                    "name": username,
                    "created": created,
                    "rent_price":rent_price,
                    "water_usage_price":water_usage_price,
                    "electricity_rate":electricity_rate,
                    "internet_price":internet_price,
                    "updated": updated,
                    "deadline": deadline,  
                }
                return Response(response)
            
            response = {
                "success":False,
                "message":"Could not process the request"
                }
            return Response(response)
        
        except Exception as e:
            return Response(e, serializer.errors)


    def create(self, request, *args, **kwargs):
        serializer = AgreementSerializer(data=request.data)
        if not serializer.is_valid():
            response = {
                "success": False,
                "message": "Invalid request"
            }
            return Response(response)
        
        try:
            tenant = serializer.validated_data['tenant']
            price =  serializer.validated_data['price']
            internet_price =  serializer.validated_data['internet_price']
            water_usage_price =  serializer.validated_data['water_usage_price']
            electricity_rate =  serializer.validated_data['electricity_rate']
            created = serializer.validated_data['created']
            updated = serializer.validated_data['updated']
            deadline = serializer.validated_data['deadline']
            
            obj = Agreement.objects.get(tenant=tenant)

            if not obj:
                instance = Agreement.objects.create(tenant=tenant, 
                           created=created,
                           updated=updated,
                           deadline=deadline, 
                           price=price, 
                           water_usage_price=water_usage_price, 
                           electricity_rate=electricity_rate, 
                           internet_price=internet_price )
                instance.save()
                response = {
                    "success": True,
                    "message": "Successfully formed contract",
                    "data": serializer.data
                }
                return Response(response)
            
            obj.updated = updated
            obj.save()

            response = {
                "success":True,
                "message":"successfully updated the contract agreement",
                "updated": updated,
                "new deadline": deadline
            }
            return Response(response)

        except Exception as e:
            return Response(e, serializer.errors)




class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

