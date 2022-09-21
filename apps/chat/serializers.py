from rest_framework.serializers import ModelSerializer
from .models import Message

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['receiver', 'message']

class AllMessageSerializers(ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'
    
class GetMessageSerializer(ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'