from django.shortcuts import get_object_or_404
from rentassist.settings import EMAIL_HOST_USER
from rentassist.utils.response import exception_response, prepare_response
from django.core.mail import send_mail
from rentassist.utils.views import AuthByNoneMixin, AuthByTokenMixin
from rest_framework.generics import GenericAPIView
from users.models import CustomUser, EmailVerification, Owner, Tenant
from .serializers import CustomUserDetailsSerializer, CustomuserSerializer, EmailVerifySerializer, OwnerDetailSerializer, TenantCreationSerializer, TenantSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

class TenantViewSet(AuthByTokenMixin, ModelViewSet):
    """ Only Available for owners"""
    serializer_class = TenantSerializer
    queryset = Tenant.objects.all()

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = Tenant.objects.filter(owner = request.user.id)
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
        queryset =  Tenant.objects.filter(owner__owner = request.user.id)
        serializer = TenantSerializer(queryset, many=True)
        return Response(serializer.data)
        

    def retrieve(self, request, pk=None, *args, **kwargs):

        queryset = Tenant.objects.filter(owner__owner = request.user.id)
        print('retreive is hit')
        tenant = get_object_or_404(queryset, pk = pk)
        serializer = TenantSerializer(tenant)
        return Response(serializer.data)


class TenantCreationAPIView(AuthByTokenMixin, GenericAPIView):
    serializer_class = TenantCreationSerializer
    def post(self, request, *args, **kwargs):

        serializer = TenantCreationSerializer(data=request.data)
        print('this api hit')
        if not serializer.is_valid():
           response=prepare_response(
               success=False,
               message='Invalid Request'
           )
           return Response(response)
        try:

            tenant = serializer.validated_data['tenant']
            owner = request.user
            id = Owner.objects.get(owner = owner)
            print(id)
            obj = Tenant.objects.filter(tenant=tenant, owner=owner.id).first()
            if not obj:
                Tenant.objects.create(tenant=tenant, owner=id)
                response = prepare_response(
                   success=True,
                   message='created successfully',
                   data=serializer.data
                )
                return Response(response)
            else:
                response = prepare_response(
                   success=False,
                   message='Already exists tenant to this owner',
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


class UserDetailsAPIView(AuthByTokenMixin, GenericAPIView):
    serializer_class = CustomUserDetailsSerializer
    queryset = CustomUser.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = CustomUser.objects.get(pk= request.user.id)
        serializer = CustomUserDetailsSerializer(queryset,many=False)
        response = prepare_response(
            success=True, 
            message = 'User details fetched successfully',
            data= serializer.data
        )
        return Response(response)


class AllUsersViewSet(AuthByNoneMixin, ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomuserSerializer


class MyOwnerDetailsView(AuthByTokenMixin, GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = OwnerDetailSerializer


    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() and request.user.is_owner:
            response = prepare_response(
                success=False,
                message='owner cant fetch this api'
            )
            return Response(response)
        
        id = CustomUser.objects.get(pk= request.user.id) 
        queryset =  Tenant.objects.filter(tenant= id)
        if queryset.exists():
            res = Tenant.objects.get(tenant=id)
            owner = res.owner.owner
            owner_firstname = owner.first_name
            owner_lastname = owner.last_name
            owner_isactive = owner.is_active
            owner_username = owner.username
            owner_phone_number = str(owner.phone_number)
            if queryset:
                response = {
                    "success": True,
                    "message": "Owner details fetched successfully",
                    "details": {
                        "first_name": owner_firstname,
                        "last_name": owner_lastname,
                        "email": owner_username,
                        "is_active": owner_isactive,
                        "owner_phone_number": owner_phone_number
                    }
                }
                return Response(response)
             
        else:
            response = {
                "success": False,
                "message": "Not registered as a Tenant"
            }
            return Response(response)