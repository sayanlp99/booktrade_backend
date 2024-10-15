import uuid
from django.db import models

class ExchangeRequest(models.Model):
    EXCHANGE_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('modified', 'Modified'),
    ]

    exchange_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    initiator = models.UUIDField()
    acceptor = models.UUIDField()
    initiator_book_id = models.UUIDField()
    acceptor_book_id = models.UUIDField()
    created_on = models.BigIntegerField()
    delivery_method = models.CharField(max_length=255)
    exchange_duration = models.IntegerField()
    request_status = models.CharField(max_length=10, choices=EXCHANGE_STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"Exchange {self.exchange_id} - {self.request_status}"
