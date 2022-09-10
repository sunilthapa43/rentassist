from django.shortcuts import render
from requests import Response
from rentassist.utils.response import prepare_response

from rentassist.utils.views import AuthByTokenMixin
from users.models import Owner, Tenant
from .serializers import TenantSerializer
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