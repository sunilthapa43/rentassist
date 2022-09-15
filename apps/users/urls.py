from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import  TenantViewSet




urlpatterns = [
    path('my-tenants/', TenantViewSet.as_view({'get':'list' , 'post':'create'}), name='my_tenants'),
    path('my-tenants/<int:pk>', TenantViewSet.as_view({'get':'retrieve', 'delete':'destroy'}), name='my_tenants'),


]