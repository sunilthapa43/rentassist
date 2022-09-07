from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import  TenantViewSet, NotificationViewSet, RentViewSet



router = SimpleRouter()
router.register('tenants', TenantViewSet, basename= 'tenants')



router.register('rent', RentViewSet, basename= 'rent')


# router.register('complaints', ComplaintViewSet, basename= 'complaint')
router.register('notifications', NotificationViewSet, basename= 'notification')


urlpatterns = router.urls


