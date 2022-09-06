from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='chat', on_delete=models.PROTECT, verbose_name='sender')
    receiver = models.ForeignKey(User, related_name='chat', on_delete=models.PROTECT, verbose_name='receiver')
    message = models.TextField()
    is_read = models.BooleanField(default=False, verbose_name='is read')
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['sent_at']