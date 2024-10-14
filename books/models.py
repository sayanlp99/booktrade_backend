from django.db import models
from authentication.models import UserProfile

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    condition = models.CharField(max_length=50)
    availability_status = models.BooleanField(default=True)
    owner = models.UUIDField()

    def __str__(self):
        return self.title
