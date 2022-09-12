
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import CustomUser, EmailVerification, Tenant
from allauth.account.adapter import get_adapter

class CustomRegisterSerializer(RegisterSerializer):
    is_owner = serializers.BooleanField(default=False)
    phone_number = serializers.CharField(max_length = 14,)
    image = serializers.ImageField(required=False)
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'is_owner',
            'image',
            'phone_number',
            'image',
            )
    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
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
        user.image = self.cleaned_data.get('image')
        user.save()
        adapter.save_user(request, user, self)
        return user






class CustomUserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'pk',
            'email',
            'phone_number',
            'is_owner',
        )



class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = '__all__'


class EmailVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerification
        fields = ('token',)