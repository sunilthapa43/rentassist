from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import  TenantViewSet, NotificationViewSet, RentViewSet



router = DefaultRouter()
router.register('my-tenants/', TenantViewSet, basename= 'tenants')
router.register('rent', RentViewSet, basename= 'rent')

# router.register('complaints', ComplaintViewSet, basename= 'complaint')
router.register('notifications', NotificationViewSet, basename= 'notification')


urlpatterns = router.urls


