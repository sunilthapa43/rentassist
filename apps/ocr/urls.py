from django.urls import include, path
from .views import ElectricityUnitView,ConfigureMeterAPIView, RunOcrAPIView
urlpatterns = [
    path('caclculate-batti', ElectricityUnitView.as_view(), name='caclculate_batti'),
    path('config-meter', ConfigureMeterAPIView.as_view(), name='config_meter'),
    path('run-ocr', RunOcrAPIView.as_view(), name='run_ocr')
]