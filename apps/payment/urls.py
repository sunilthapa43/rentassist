from django.urls import path

from .views import KhaltiVerifyView
urlpatterns =[
    path('',KhaltiVerifyView.as_view(), name='verify payment')
]