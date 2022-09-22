from datetime import datetime
from decimal import Decimal
from yaml import serialize
from payment.khalti import Khalti
from users.models import Tenant
from rentassist.settings import BASE_DIR
from rentassist.utils.views import AuthByTokenMixin
from .serializers import AllTransactionSerializer, KhaltiVerifySerializer, OtherPaymentSerializer
from rentassist.utils.response import exception_response, prepare_response
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .models import AllTransaction, Transaction
from rest_framework.viewsets import ModelViewSet


# generate pdf
import io
import os
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
path_to_image = 'apps/payment/logo/logo.png'
image_path = os.path.join(BASE_DIR, path_to_image) 
def background(c):
    c.setFillColorRGB(1,0,0)
    c.setFont('Helvetica-Bold', 15)
    c.rect(5,5,652,792,fill=0)

class KhaltiVerifyView(AuthByTokenMixin, GenericAPIView):
    serializer_class=KhaltiVerifySerializer
    queryset = Transaction.objects.all()
    def post(self, request, *args, **kwargs):
        serializer = KhaltiVerifySerializer(data=request.data)
        if not serializer.is_valid():
            response = prepare_response(success=False,
                                        message='Invalid data',
                                        errors=serializer.errors)
            return Response(response, status=400)

        # khalti = Khalti(user=self.request.user,
        #                 token=serializer.validated_data['payment_token'],
        #                 amount=serializer.validated_data['paid_amount'],
        #                 )

        # payment_response = khalti.verify_request()
        # print(payment_response)
        # if 'idx' in payment_response:\

        paid_amount=serializer.validated_data['paid_amount'] 
        paid_amount = paid_amount/100          
        payment_token=serializer.validated_data['payment_token']
        user = request.user
        t = Tenant.objects.get(tenant = user)
        
        print(t.tenant.tenant.owner)
        obj = Transaction.objects.create(
            initiator=t,
            paid_amount=paid_amount,         
            payment_token= payment_token
            )
        obj.save()
        if obj:
            # create buffer:
            buffer = io.BytesIO()
            # buttom up =1 for image to be not inverted
            c = canvas.Canvas(buffer, pagesize=letter, bottomup=1)
            background(c)
            # c.translate(cm,cm)
            c.setPageSize((300,300))
            # c.circle(150,150,100)
            
            c.drawImage(image_path, x=120, y=250, width=50, height=50)
            info_obj = c.beginText(50,220)
            username = str(t.tenant.first_name) + ' ' + str(t.tenant.last_name)
            paid_to = str(t.owner.owner.first_name) + ' ' + str(t.owner.owner.last_name)
            time =  datetime.now()
            paid_at = str(time.strftime("%Y-%m-%d  %H:%M:%S"))
            print(paid_to)
            lines = [
        
            ]
            
            lines.append('TRANSCATION   DETAILS       '),
            lines.append('             '),
            lines.append('initiator : ' + username),
            
            lines.append('paid to:  ' + paid_to)
            lines.append('paid at :    ' + paid_at)
            
            lines.append('amount:  ' + str(paid_amount))
            lines.append('more details: ')
            lines.append('token:   ' + payment_token)
            lines.append('currency:   NPR')
    
            for line in lines:
                info_obj.textLine(line)    
            c.drawText(info_obj)
            c.showPage()
            c.save()
            buffer.seek(0)
        
            return FileResponse(buffer, as_attachment=True, filename='invoice.pdf')
        

        else:
            response = prepare_response(success=False,
                                        message='Payment Unsuccessful, Try Agaiin',
                                        data=serializer.data)
            return Response(response)



class OtherPaymentAPIView(AuthByTokenMixin, GenericAPIView):
    """Can only be added by the owner himself"""
    
    serializer_class = OtherPaymentSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            response = prepare_response(success=False,
                                        message='Invalid data',
                                        errors=serializer.errors)
            return Response(response, status=400)
        
        else:
            if not request.user.is_owner:
                response = prepare_response(success=False,
                                        message='Only owner can use this API to update balance',
                                        )
                return Response(response)
            try:
                response = prepare_response(success=True,
                                            message=f'Payment successful',
                                            data=serializer.data
                                            )
                return Response(response, status=200)
            except Exception as e:
                return exception_response(e, serializer)

    
class AllTransactionsAPIView(AuthByTokenMixin, ModelViewSet):
    serializer_class = AllTransactionSerializer
    queryset = AllTransaction.objects.all()
    def list(self, request, *args, **kwargs):
        if request.user.is_owner:
            queryset = AllTransaction.objects.filter(initiator__tenant__tenant__owner__owner = request.user.id)
            print(queryset)
            serializer = AllTransactionSerializer(queryset, many=True)
            response = prepare_response(
                success=True,
                messge='fetched successfully',
                data=serializer.data
            )
            return Response(response)
        
        elif not request.user.is_owner:
            queryset = AllTransaction.objects.filter(initiator__tenant = request.user)
            serializer = AllTransactionSerializer(queryset, many=True)
            response ={
                "success":True,
                "message" : 'Your transaction history fetched successfully',
                "data":serializer.data
            }
            return Response(response)