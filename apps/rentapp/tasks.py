from celery import shared_task
from documents.models import Agreement
from rentapp.models import Rent
from datetime import datetime, timedelta
    

@shared_task
def check_deadline(*args):
    all = Rent.objects.filter(next_payment_schedule = datetime.now().date() + timedelta(days=1))
    (a.create_notification(days = 1, flag = 0) for a in all)
    (a.create_notification(days=1, flag=1) for a in all)
    today = Rent.objects.filter(next_payment_schedule = datetime.now().date())
    (a.create_notification(days=0, flag=0) for a in today)
    (a.create_notification(days= 0, flag=1) for a in today)
    skipped = Rent.objects.filter(next_payment_schedule = datetime.now().date() - timedelta(days=1))
    (a.create_notification(days=-1, flag=0) for a in skipped)
    (a.create_notification(days=-1, flag=1) for a in skipped)


@shared_task
def check_agreement_status(*args):
    today = Agreement.objects.filter(deadline =  datetime.now().date())
    (t.create_notification(days=0, flag=1) for t in today)
    (t.create_notification(days=0, flag=0) for t in today)

    skipped =  Agreement.objects.filter(deadline = datetime.now().date() - timedelta(days=2))
    (s.create_notification(days=-1, flag=1) for s in skipped)
    (s.create_notification(days=-1, flag=0) for s in skipped)
