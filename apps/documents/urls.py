from rest_framework.routers import DefaultRouter
from .views import AgreementViewSet
router = DefaultRouter()


router.register('agreements', AgreementViewSet, basename= 'agreement')

urlpatterns = router.urls