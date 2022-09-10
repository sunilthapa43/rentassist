from payment.khalti import Khalti
from rentapp.models import Tenant
from rentassist.settings import BASE_DIR
from rentassist.utils.views import AuthByTokenMixin
from .serializers import KhaltiVerifySerializer, OtherPaymentSerializer
from rentassist.utils.response import exception_response, prepare_response
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .models import Transaction


# generate pdf
import io
import os
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
path_to_image = 'static/images/logo.png'
image_path = os.path.join(BASE_DIR, path_to_image) 
def background(c):
    c.setFillColorRGB(1,0,0)
    c.setFont('Helvetica-Bold', 15)
    c.rect(5,5,652,792,fill=1)

class KhaltiVerifyView(AuthByTokenMixin, GenericAPIView):
    serializer_class=KhaltiVerifySerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            response = prepare_response(success=False,
                                        message='Invalid data',
                                        errors=serializer.errors)
            return Response(response, status=400)

        khalti = Khalti(user=self.request.user,
                        token=serializer.data['token'],
                        amount=serializer.data['paid_amount'],
                        )

        payment_response = khalti.verify_request()
        if 'idx' in payment_response:
            Transaction.objects.create(
                initiator=self.request.user,
                paid_amount=payment_response['amount'],
                payment_token=payment_response['token'],
                transaction_response=payment_response)

            response = prepare_response(success=True,
                                        message='Payment successful',
                                        data=payment_response)
            return Response(response, status=200)
        else:
            response = prepare_response(success=False,
                                        message='Payment failed',
                                        data=payment_response)
            return Response(response, status=400)
    
    def get(self, request, *args, **kwargs):
    # TODO: check the response of the khalti verification then provide the details

        # create buffer:
        buffer = io.BytesIO()
        # buttom up =1 for image to be not inverted
        c = canvas.Canvas(buffer, pagesize=letter, bottomup=1)
        background(c)
        # c.translate(cm,cm)
        c.setPageSize((300,300))
        # c.circle(150,150,100)
        
        c.drawImage(image_path, x=0, y=0, width=300, height=300)
        info_obj = c.beginText(50,250)
        initiator = request.user
        print(initiator)
        username = request.user.username
        _tenant = Tenant.objects.get(tenant=initiator)
        paid_to = _tenant.owner.username
        print(paid_to)
        # amount = request.GET.get['amount']
        transaction = Transaction.objects.get(initiator=initiator, transaction_status='SUCCESS')
        print(transaction)
    
        lines = [
    
        ]
        
        lines.append('TRANSCATION   DETAILS       '),
        lines.append('             '),
        lines.append('initiator : ' + username),
        lines.append('')
        lines.append('paid to:  ' + paid_to)

        lines.append('')
        lines.append('amount:  ' + str(transaction.payment_response['amount']))
        lines.append('more details: ')
        lines.append('token:   ' + transaction.payment_response['token'])
        lines.append('currency:  '+ transaction.payment_response['currency'])

        for line in lines:
            info_obj.textLine(line)    
        c.drawText(info_obj)
        c.showPage()
        c.save()
        buffer.seek(0)
    
        return FileResponse(buffer, as_attachment=True, filename='invoice.pdf')


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