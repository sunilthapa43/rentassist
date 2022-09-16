from datetime import datetime, timedelta
from django.dispatch import Signal

from documents.models import Agreement

#sending and making signals

# agreement_deadline_approach = Signal()
# approaching_deadlines = Agreement.objects.filter(deadline = datetime.now().date()+timedelta(days=2))
# if approaching_deadlines:
#     for all in approaching_deadlines:
#         type(all).agreement_deadline_approach.send(sender=Agreement)


# agreement_deadline_skipped =  Signal()
# skipped_deadlines = Agreement.objects.filter(deadline = datetime.now().date() - timedelta(days=1))
# if skipped_deadlines:
#     for all in skipped_deadlines:
#         agreement_deadline_skipped.send()
#     #receiver(deadline_notification)