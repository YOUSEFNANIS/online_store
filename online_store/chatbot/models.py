from django.db import models
from users.models import User
from django.utils import timezone
class chat(models.Model):

    creation_time = models.DateTimeField(default = timezone.now)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    
class ChatMessage(models.Model):
    creation_time = models.DateTimeField(default = timezone.now)
    chat = models.ForeignKey(to=chat, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField(blank=True)

class Meta:
        ordering = ['creation_time']

