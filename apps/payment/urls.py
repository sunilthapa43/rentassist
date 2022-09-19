from django.urls import path

from .views import AllTransactionsAPIView, KhaltiVerifyView
urlpatterns =[
    path('',KhaltiVerifyView.as_view(), name='verify payment'),
    path('my-transactions', AllTransactionsAPIView.as_view())
]