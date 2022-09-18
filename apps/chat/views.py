
from django.core import serializers

from rest_framework.response import Response

from .serializers import MessageSerializer, MessageViewSerializer

from rentassist.utils.views import AuthByTokenMixin
from .models import Message
from rest_framework.generics import GenericAPIView


class ChatAPIView(AuthByTokenMixin, GenericAPIView):
    serializer_classes = [MessageSerializer, MessageViewSerializer]
    def get(self, request, *args, **kwargs):
        serializer = MessageViewSerializer(data=request.data)
        if serializer.is_valid():
            sender = request.user
            receiver = serializer.validated_data['receiver']
            sent_message = Message.objects.filter(sender=sender, receiver=receiver)
            received_message = Message.objects.filter(sender=receiver, receiver=sender)
            if sent_message.exists() or received_message.exists():
                sent_messages = serializers.serialize('json', sent_message)
                received_messages = serializers.serialize('json', received_message)
                for msg in received_message:
                    msg.is_read=True
                    msg.save()
                response = {
                    "succes":True,
                    "message":"Successfully fetched the conversation",
                    "sent_message":sent_messages,
                    "received_message": received_messages
                }
                return Response(response)
            response ={
                "success":True,
                "message":"Inbox Empty"
            }
            return Response(response)
        response = {
            "success": False,
            "message": 'Invalid request'
        }
        return Response(response)
    
    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            sender = request.user
            receiver = serializer.validated_data['receiver']
            message = serializer.validated_data['message']
            obj = Message.objects.create(sender = sender, receiver=receiver, message=message)
            if obj:
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

