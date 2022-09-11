from ast import Return
from celery import shared_task
from notification.models import Notification

from rentapp.models import Rent
from datetime import datetime, timedelta
    

@shared_task
def check_deadline():
    all = Rent.objects.filter(next_payment_schedule = datetime.now().date() + timedelta(days=1))
    (a.create_notification(days = 1, flag = 0) for a in all)
    (a.create_notification(days=1, flag=1) for a in all)
    today = Rent.objects.filter(next_payment_schedule = datetime.now().date())
    (a.create_notification(days=0, flag=0) for a in today)
    (a.create_notification(days= 0, flag=1) for a in today)
    skipped = Rent.objects.filter(next_payment_schedule = datetime.now().date() - timedelta(days=1))
    (a.create_notification(days=-1, flag=0) for a in skipped)
    (a.create_notification(days=-1, flag=1) for a in skipped)