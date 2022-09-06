from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from .serializers import MessageSerializer, MessageViewSerializer

from rentassist.utils.views import AuthByTokenMixin
from .models import Message
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
User = get_user_model

class ChatAPIView(AuthByTokenMixin, GenericAPIView):
    serializer_classes = [MessageSerializer, MessageViewSerializer]
    def get(self, request, *args, **kwargs):
        serializer = MessageViewSerializer(data=request.data)
        if serializer.is_valid():
            sender = serializer.validated_data['sender']
            receiver = serializer.validated_data['receiver']
            message = Message.objects.filter(sender=sender, receiver=receiver) | Message.objects.filter(sender=receiver, receiver=sender)
            if message.exists():
                for msg in message:
                    msg.is_read =True
                    msg.save()
            response = {
                "succes":True,
                "message":message,
                "data": serializer.data
            }
        
            return Response(response)
    
    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "success":True,
                "data":serializer.data,
                "message":"Message sent successfully"
            }
            return Response(response)
        response = {
            "success":False,
            "message":"Sorry, could not process request"
        }
        return Response(response)

