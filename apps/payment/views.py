from payment.khalti import Khalti

from rentassist.utils.views import AuthByTokenMixin
from .serializers import KhaltiVerifySerializer
from rentassist.utils.response import prepare_response
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .models import Transaction

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
                        amount=serializer.data['amount'],
                        )

        payment_response = khalti.verify_request()
        if 'idx' in payment_response:

            Transaction.objects.create(
                initiator=self.request.user,
                amount=payment_response['amount'],
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
    
