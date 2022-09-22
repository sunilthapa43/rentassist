from django.db import models
from django.contrib.auth import get_user_model
from users.models import Tenant

User = get_user_model()

NOTIFICATION_TYPES = [
    ('D', 'Deadline Approach'),
    ('S', 'Deadline Skipped'),
    ('C', 'Complaint'),
    ('P', 'Payment'),
    ('O', 'Other Payment'),
    ('A', 'Agreement Formed'),
    ('CE', 'Contract Extended'),
    ('E', 'Contract Expiry'),
    ('CM', 'Configure Meter'),
    
]

class Notification(models.Model):
    created = models.DateTimeField(auto_now=True)
    tenant =  models.ForeignKey('users.Tenant', on_delete=models.CASCADE, verbose_name='Tenant', related_name='notification')
    is_read = models.BooleanField(default=False)
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name='Title')
    type = models.CharField(choices=NOTIFICATION_TYPES, max_length=30, verbose_name='type of notification', blank=False)
    target = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Notification target')
    deep_link = models.CharField(max_length=70, default = 'rentassist2021/api/notifications')

    def __str__(self) -> str:
        return f'triggered by {self.tenant} received by {self.target.username} '
