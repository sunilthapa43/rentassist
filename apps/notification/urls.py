from django.urls import path , include
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from .views import NotificationAPIView


urlpatterns = [
    path(
        'notification/',
        NotificationAPIView.as_view(),
        name='notification',
    ),
    path('devices/', FCMDeviceAuthorizedViewSet.as_view({'post':'create'}), name='devices'),
]