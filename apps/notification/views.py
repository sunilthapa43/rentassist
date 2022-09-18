from rest_framework.response import Response
from notification.models import Notification
from notification.serilaizers import NotificationSerializer
from rest_framework.generics import GenericAPIView
from rentassist.utils.views import AuthByTokenMixin
from rentassist.utils.response import prepare_response
class NotificationAPIView(AuthByTokenMixin, GenericAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    def get(self, request, *args, **kwargs):
        queryset = Notification.objects.filter(target=request.user)
        
        for all in queryset:
            all.is_read=True
            all.save()

        serializer = NotificationSerializer(queryset, many=True)

        response = prepare_response(
            success=True,
            message ='fetched successfully',
            data=serializer.data
        )
        return Response(response)
        
