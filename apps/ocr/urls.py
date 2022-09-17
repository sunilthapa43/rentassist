from django.urls import include, path
from .views import ElectricityUnitView,ConfigureMeterAPIView
urlpatterns = [
    path('scan-batti', ElectricityUnitView.as_view(), name='scan_batti'),
    path('config-meter', ConfigureMeterAPIView.as_view(), name='config_meter'),

]