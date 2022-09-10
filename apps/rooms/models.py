from django.db import models
from django.contrib.auth import get_user_model

from users.models import Owner

User = get_user_model()

class Room(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name='owner', related_name='rooms')