from django.urls import path
from .views import ChatAPIView, FetchAllMessages

urlpatterns = [
    path('inbox/',ChatAPIView.as_view(), name='chat'),
    path('', FetchAllMessages.as_view({'get':'list'}), name='all_messages')
]