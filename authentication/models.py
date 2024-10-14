from django.db import models
import uuid

class UserProfile(models.Model):
    username = models.CharField(max_length=30)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    otp = models.BigIntegerField(null=True, blank=True)
    reading_preferences = models.TextField(blank=True)
    favorite_genres = models.CharField(max_length=255, blank=True)
    email_verified = models.BooleanField(default=False, null=True, blank=True)
    user_registered = models.BooleanField(default=False, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
