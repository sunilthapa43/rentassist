from datetime import datetime, timedelta
from django.dispatch import Signal

from documents.models import Agreement

#sending and making signals

deadline_approach = Signal()
approaching_deadlines = Agreement.objects.filter(deadline = datetime.now().date()+timedelta(days=2))
for all in approaching_deadlines:
    all.deadline_approach.send()


deadline_skipped =  Signal()
skipped_deadlines = Agreement.objects.filter(deadline = datetime.now().date() - timedelta(days=1))
for all in skipped_deadlines:
    all.deadline_skipped.send()
#receiver(deadline_notification)