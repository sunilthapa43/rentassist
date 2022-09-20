from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ComplaintViewSet, RentViewSet, RoomViewSet



router = DefaultRouter()
router.register('rent', RentViewSet, basename= 'rent')
router.register('rooms', RoomViewSet, basename='room')
router.register('complaints',ComplaintViewSet, basename= 'complaint')
# router.register('notifications', NotificationViewSet, basename= 'notification')


urlpatterns = router.urls


