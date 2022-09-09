from rest_framework.routers import DefaultRouter
from .views import  TenantViewSet



router = DefaultRouter()
router.register('my-tenants/', TenantViewSet, basename= 'tenants')

urlpatterns = router.urls