
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

from .models import CustomUser, EmailVerification, Tenant
from allauth.account.adapter import get_adapter

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length = 25, required=True)
    last_name = serializers.CharField(max_length = 25, required=True)
    is_owner = serializers.BooleanField(default=False)
    phone_number = serializers.CharField(max_length = 14,)
    image = serializers.ImageField(required=False)
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'is_owner',
            'image',
            'phone_number',
            'image',
            )
    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'email': self.validated_data.get('email', ''),
            'is_owner': self.validated_data.get('is_owner'),
            'phone_number': self.validated_data.get('phone_number'),
            'image': self.validated_data.get('image'),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.phone_number = self.cleaned_data.get('phone_number')
        user.is_owner = self.cleaned_data.get('is_owner')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.image = self.cleaned_data.get('image')
        user.save()
        adapter.save_user(request, user, self)
        return user


class CustomUserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'is_active',
            'is_owner',
            'phone_number',
            'first_name',
            'last_name',
            'image')





class TenantSerializer(serializers.ModelSerializer):

    def get_fname(self, obj):
        return obj.f_name()

    def get_lname(self, obj):
        return obj.l_name()
    
    def get_email(self, obj):
        return obj.email()

    def get_phone(self, obj):
        return obj.get_phone()


    def to_representation(self, instance):
       response =  super().to_representation(instance)
       response['first_name'] = instance.tenant.first_name
       response['last_name'] = instance.tenant.last_name
       response['email'] = instance.tenant.email
       response['phone_number'] = str(instance.tenant.phone_number)
       
       return response
        
    class Meta:
        model = Tenant
        fields = '__all__'
    

   
class TenantCreationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tenant
        fields = ('owner',)


class EmailVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerification
        fields = ('token',)


class CustomuserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields ='__all__'



class OwnerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model =Tenant
        exclude = ('tenant', 'owner')