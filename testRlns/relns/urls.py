
from posixpath import basename
from rest_framework.routers import SimpleRouter
from .views import OwnerViewSet, TenantViewSet, ChatViewSet

router = SimpleRouter()
router.register('owners', OwnerViewSet , basename = 'owners')
router.register('tenants', TenantViewSet , basename = 'tenants')
router.register('chat', ChatViewSet , basename = 'get-chatlist')
router.register('chat/(?P<sender>.+)&(?P<receiver>.+)', ChatViewSet, basename = 'chat-list'),



urlpatterns = router.urls
