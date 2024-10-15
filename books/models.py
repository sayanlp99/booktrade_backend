from django.db import models
from authentication.models import UserProfile
import uuid

class Book(models.Model):
    book_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    condition = models.CharField(max_length=50)
    availability_status = models.BooleanField(default=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    owner = models.UUIDField()
