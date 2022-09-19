"""rentassist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from baton.autodiscover import admin
from django.urls import path, include
# from rest_framework import permissions
from users.views import VerifyToken

# configure drf-yasg docs
# from drf_yasg.views import get_schema_view # new
# from drf_yasg import openapi # new
# schema_view = get_schema_view(
#      # new
#     openapi.Info(
#         title="Blog API",
#         default_version="v1",
#         description="A sample API for learning DRF",
#         terms_of_service="https://www.google.com/policies/terms/",
#         contact=openapi.Contact(email="hello@example.com"),
#         license=openapi.License(name="BSD License"),
#         ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
#     )





urlpatterns = [
    path('admin/', admin.site.urls),
    path('baton/', include('baton.urls')),
    path('api/', include('rentapp.urls')),
    path('api/payment/', include('payment.urls')),
    path('api/ocr/', include('ocr.urls')),
    path('chat/', include('chat.urls')),
    path('api/notifications/', include('notification.urls')),
    path('api/users/',include('users.urls')),

    #agreements
    path('api/contract/', include('documents.urls')),
    #user registration
    path('auth/register/', include('dj_rest_auth.registration.urls')),
    path('auth/', include('dj_rest_auth.urls')),  #login, logout, pwreset  

    # from users
    path('auth/verify-email/', VerifyToken.as_view({'post':'create'})),

]
