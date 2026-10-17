from django.conf import settings
from django.db import models
from users.models import seller, customer
from core.models import product


class Conversation(models.Model):
    # One thread per customer/seller pair, like an Alibaba trade-manager chat.
    customer = models.ForeignKey(to=customer, on_delete=models.CASCADE, related_name='conversations')
    seller = models.ForeignKey(to=seller, on_delete=models.CASCADE, related_name='conversations')
    last_message_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'seller')
        ordering = ['-last_message_at', '-id']


class Message(models.Model):
    conversation = models.ForeignKey(to=Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(max_length=2000)
    # Product the message is about (inquiry card shown in the thread)
    product = models.ForeignKey(to=product, on_delete=models.SET_NULL, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['creation_date', 'id']
