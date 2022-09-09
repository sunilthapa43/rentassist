from .models import Tenant
from rest_framework import viewsets
from .serializers import TenantSerializer
class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer