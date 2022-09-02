from django.urls import include, path
from .views import ElectricityUnitView
urlpatterns = [
    path('scan-batti', ElectricityUnitView.as_view(), name='scan_batti')
]