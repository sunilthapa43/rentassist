from email import message
from urllib import response
from django.shortcuts import get_object_or_404, render
from requests import Response
from rentassist.settings import EMAIL_HOST_USER
from rentassist.utils.response import exception_response, prepare_response
from django.core.mail import send_mail
from rentassist.utils.views import AuthByNoneMixin, AuthByTokenMixin
from users.models import EmailVerification, Owner, Tenant
from .serializers import EmailVerifySerializer, TenantSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

class TenantViewSet(AuthByTokenMixin, ModelViewSet):
    def list(self, request, *args, **kwargs):
        if not request.user.is_owner:
            response = prepare_response(
                success=False,
                message = 'You are not allowed to fetch this API'
            )
            return Response(response)
        owner = Owner.objects.get(owner = request.user).id
        queryset =  Tenant.objects.filter(owner=owner)
        serializer = TenantSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        owner = Owner.objects.get(owner=request.user).id
        queryset = Tenant.objects.filter(owner=owner)
        print(queryset)
        tenant = get_object_or_404(queryset, pk = pk)
        serializer = TenantSerializer(tenant)
        return Response(serializer.data)

    

class VerifyToken(AuthByTokenMixin, ModelViewSet):
    serializer_class = EmailVerifySerializer
    queryset =  EmailVerification.objects.all()
    def create(self, request, *args, **kwargs):
        serializer = EmailVerifySerializer(data= request.data)
        if not serializer.is_valid():
            response = prepare_response(
                success=False,
                message='Invalid Request'
            )
            return Response(response)
        else:
            try:
                user = request.user
                token = serializer.validated_data['token']
                obj = EmailVerification.objects.get(user=user, token=token)
                if not obj:
                    response = prepare_response(
                        success=False,
                        message='The OTP is invalid, please try again',
                        data=serializer.data
                    )
                    return Response(response)
                else:
                    obj.is_authenticated = True
                    obj.save()
                    # send mail here instead of using signals
                    send_mail(
                        'Account Verified',
                        'Your account has been verified successfully',
                        EMAIL_HOST_USER,
                        [obj.user.email]
                    )
                    response = prepare_response(
                        success=True,
                        message='Congratulations, you are considered as an active user now',
                        data=serializer.data
                    )
                    return Response(response)
                    
            except Exception as e:
                return exception_response(e, serializer)