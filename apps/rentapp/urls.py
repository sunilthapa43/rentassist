from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CompalaintViewSet, RentViewSet



router = DefaultRouter()
router.register('rent', RentViewSet, basename= 'rent')

router.register('complaints',CompalaintViewSet, basename= 'complaint')
# router.register('notifications', NotificationViewSet, basename= 'notification')


urlpatterns = router.urls


