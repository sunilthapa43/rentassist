from django.urls import path , include
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from .views import NotificationAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('devices', FCMDeviceAuthorizedViewSet, basename='devices')

urlpatterns = [
    path(
        'notification/',
        NotificationAPIView.as_view(),
        name='notification',
    ),
    path('', include(router.urls)),
]