from django.shortcuts import get_object_or_404
from rentassist.settings import EMAIL_HOST_USER
from rentassist.utils.response import exception_response, prepare_response
from django.core.mail import send_mail
from rentassist.utils.views import AuthByTokenMixin
from users.models import EmailVerification, Owner, Tenant
from .serializers import EmailVerifySerializer, TenantCreationSerializer, TenantSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

class TenantViewSet(AuthByTokenMixin, ModelViewSet):
    serializer_class = TenantSerializer
    queryset = Tenant.objects.all()

    def destroy(self, request, pk=None, *args, **kwargs):
        
        
        owner = Owner.objects.get(owner = request.user).id
        print(type(owner))
        queryset = Tenant.objects.filter(owner=owner)
        
        obj = get_object_or_404(queryset, pk=pk)
        if not obj:
            response = prepare_response(
                success=False,
                message='Does not exist'
            )
            return Response(response)
        serializer = TenantSerializer(obj)
        obj.delete()
        
        response = prepare_response(
            success=True,
            message = 'successfully removed tenant',
            data=serializer.data
        )
        return Response(response)


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
        print('retreive is hit')
        tenant = get_object_or_404(queryset, pk = pk)
        serializer = TenantSerializer(tenant)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = TenantCreationSerializer(data=request.data)
        if not serializer.is_valid():
            response=prepare_response(
                success=False,
                message='Invalid Request'
            )
            return Response(response)
        try:
            tenant = serializer.validated_data['tenant']
            owner = serializer.validated_data['owner']
            print(request.user.id)
            obj = Tenant.objects.get_or_create(tenant=tenant, owner=owner)
            if obj:
                response = prepare_response(
                    success=True,
                    message='created successfully',
                    data=serializer.data
                )
                return Response(response)
            else:
                response = prepare_response(
                    success=False,
                    message='Could not create user',
                    data=serializer.data
                )
                return Response(response)
                
        except Exception as e:
            return exception_response(e, serializer)        


    

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