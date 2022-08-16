from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ChatSerializer, OwnerSerializer, TenantSerializer

# Create your views here.


from .models import Owner, Tenant, Chat

class OwnerViewSet(viewsets.ModelViewSet):
    serializer_class =  OwnerSerializer
    queryset =  Owner.objects.all()


class TenantViewSet(viewsets.ModelViewSet):
    serializer_class =  TenantSerializer
    queryset =  Tenant.objects.all()


class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()

    def get_queryset(self):
        queryset = Chat.objects.all()
        sender =  self.request.query_params.get('sender')
        receiver =  self.request.query_params.get('receiver')

        if sender is not None and receiver is not None:
            queryset1 = Chat.objects.filter(sender=sender,receiver=receiver)
            queryset2 = Chat.objects.filter(sender=receiver,receiver=sender)
            queryset =  queryset1.union(queryset2)

            return queryset

