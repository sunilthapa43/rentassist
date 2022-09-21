from django.urls import path
from .views import ChatAPIView, FetchAllMessages, GetConversationViewSet

urlpatterns = [
    path('send-message/',ChatAPIView.as_view(), name='send_message'),
    path('inbox/',GetConversationViewSet.as_view({'get':'list'}), name='inbox' ),
    path('', FetchAllMessages.as_view({'get':'list'}), name='all_messages')
]