from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import OwnerViewSet, TenantViewSet, DepositViewSet, DocumentViewSet, ElectricityViewSet, OtherPaymentViewSet, NotificationViewSet, RentViewSet, TransactionViewSet, AgreementViewSet, ComplaintViewSet



router = SimpleRouter()
router.register('owners', OwnerViewSet, basename= 'owners')
router.register('tenants', TenantViewSet, basename= 'tenants')
router.register('deposit', DepositViewSet, basename= 'deposit')
router.register('documents', DocumentViewSet, basename= 'documents')
router.register('electricity', ElectricityViewSet, basename= 'electricity')
router.register('other-payment', OtherPaymentViewSet, basename= 'other-ayment')
router.register('rent', RentViewSet, basename= 'rent')
router.register('transaction', TransactionViewSet, basename= 'transaction')
router.register('agreements', AgreementViewSet, basename= 'agreement')
router.register('complaints', ComplaintViewSet, basename= 'complaint')
router.register('notifications', NotificationViewSet, basename= 'notification')


urlpatterns = router.urls
