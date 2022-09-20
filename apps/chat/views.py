
from django.core import serializers
from django.dispatch import receiver

from rest_framework.response import Response

from rentassist.utils.response import prepare_response

from .serializers import AllMessageSerializers, MessageSerializer
from rest_framework.viewsets import ModelViewSet

from rentassist.utils.views import AuthByTokenMixin
from .models import Message
from rest_framework.generics import GenericAPIView


class ChatAPIView(AuthByTokenMixin, GenericAPIView):
    serializer_classes = MessageSerializer
    def get(self, request, *args, **kwargs):
        receiver = request.GET['friend']
        if not receiver:
           response = {
               "success": False,
               "message": 'Invalid request, need friend id to get the conversation'
           }
           return Response(response)
        sender = request.user
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


class FetchAllMessages(AuthByTokenMixin, ModelViewSet):

    serializer_class = AllMessageSerializers
    queryset = Message.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = Message.objects.filter(receiver = request.user.id).order_by('-sent_at').distinct('sender')
        serializer = AllMessageSerializers(queryset, many = True)

        response = prepare_response(
            success=True,
            message="Your messages fetched successfully",
            data= serializer.data
        )
        return Response(response)