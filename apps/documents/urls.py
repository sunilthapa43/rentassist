from rest_framework.routers import DefaultRouter
from .views import AgreementViewSet, DocumentViewSet
router = DefaultRouter()


router.register('agreement', AgreementViewSet, basename= 'agreement')
router.register('documents', DocumentViewSet, basename='document')
urlpatterns = router.urls