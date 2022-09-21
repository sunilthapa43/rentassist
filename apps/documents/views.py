
from rest_framework.response import Response
from payment.models import Transaction
from rentassist.utils.response import exception_response, prepare_response

from rentassist.utils.views import AuthByTokenMixin
from .models import Document, Agreement
from rest_framework.viewsets import ModelViewSet
from .serializers import DocumentSerializer, AgreementSerializer


class AgreementViewSet(AuthByTokenMixin, ModelViewSet):
    
    serializer_class = AgreementSerializer
    def list(self, request, *args, **kwargs):
        user = request.user
        if user.is_owner:
            queryset = Agreement.objects.filter(tenant__owner = user.id)
            serializer = AgreementSerializer(queryset, many=True)
            response = {
                "success":True,
                "message":"Successfully fetched agreements",
                "data": serializer.data
            }
            return Response(response)
        
        elif not user.is_owner:
            try:
                print(type(request.user), request.user.username)
                # _queryset = Agreement.objects.get(tenant__tenant = request.user.id)
                queryset = Agreement.objects.get(tenant__tenant = request.user.id)
                owner = queryset.tenant.owner
                print(owner)
                serializer = AgreementSerializer(queryset, many=False)
                response = {
                    "success":True,
                    "message":f"Successfully fetched your agreement with the owner: MR. {owner}",
                    "data": serializer.data
                }
                return Response(response)
            except Exception as e:
                return exception_response(e, serializer.errors)
    
        response = {
            "success":False,
            "message":"Could not process the request"
            }
        return Response(response)
        



    def create(self, request, *args, **kwargs):
        serializer = AgreementSerializer(data=request.data)
        if not serializer.is_valid():
            response = {
                "success": False,
                "message": "Invalid request"
            }
            return Response(response)
        
    
        tenant = serializer.validated_data['tenant']
        price =  serializer.validated_data['price']
        internet_price =  serializer.validated_data['internet_price']
        water_usage_price =  serializer.validated_data['water_usage_price']
        electricity_rate =  serializer.validated_data['electricity_rate']
        nagarpalika_fohr_price =  serializer.validated_data['nagarpalika_fohr_price']
        picture = serializer.validated_data['picture']
        
        obj = Agreement.objects.filter(tenant=tenant)
        if not obj.exists():
            instance = Agreement.objects.create(
                       tenant=tenant, 
                       price=price, 
                       water_usage_price=water_usage_price, 
                       electricity_rate=electricity_rate, 
                       nagarpalika_fohr_price=nagarpalika_fohr_price,
                       internet_price=internet_price,
                       picture = picture )
            instance.save()
            response = {
                "success": True,
                "message": "Successfully formed contract",
                "data": serializer.data
            }
            return Response(response)
        else:

            obj = Agreement.objects.get(tenant=tenant)
            print(obj.price)
            obj.price=price 
            obj.water_usage_price=water_usage_price 
            obj.electricity_rate=electricity_rate 
            obj.nagarpalika_fohr_price=nagarpalika_fohr_price
            obj.internet_price=internet_price 
            obj.save()
            response = prepare_response(
                success =True,
                message='successfully updated agreement',
                data=serializer.data
            )
            return Response(response)

        




class DocumentViewSet(AuthByTokenMixin, ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

