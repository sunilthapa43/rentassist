from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import  MyOwnerDetailsView, TenantViewSet, UserDetailsAPIView, AllUsersViewSet , TenantCreationAPIView




urlpatterns = [
    path('my-tenants/', TenantViewSet.as_view({'get':'list'}), name='my_tenants'),
    path('my-tenants/<int:pk>', TenantViewSet.as_view({'get':'retrieve', 'delete':'destroy'}), name='my_tenants'),
    path('my-details/', UserDetailsAPIView.as_view(), name='user'),
    path('add-tenant/', TenantCreationAPIView.as_view()),

    #for production only
    path('users/',AllUsersViewSet.as_view({'get':'list'}), name='xasdc' ),
    path('my-owner/', MyOwnerDetailsView.as_view())
]