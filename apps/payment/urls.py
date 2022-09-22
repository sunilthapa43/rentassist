from django.urls import path

from .views import AllTransactionsAPIView, KhaltiVerifyView, WithDrawView
urlpatterns =[
    path('',KhaltiVerifyView.as_view(), name='verify payment'),
    path('withdraw',WithDrawView.as_view(), name='withdraw'),

    path('my-transactions', AllTransactionsAPIView.as_view({'get':'list'}))
]