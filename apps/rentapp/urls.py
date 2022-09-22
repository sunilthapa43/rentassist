from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ComplaintViewSet, DueRentView, RentViewSet, RoomViewSet



router = DefaultRouter()
router.register('rent', RentViewSet, basename= 'rent')
router.register('rooms', RoomViewSet, basename='room')
router.register('complaints',ComplaintViewSet, basename= 'complaint')
# router.register('notifications', NotificationViewSet, basename= 'notification')


urlpatterns =[
    path('due_amount/', DueRentView.as_view()),
    path('', include(router.urls))
] 


