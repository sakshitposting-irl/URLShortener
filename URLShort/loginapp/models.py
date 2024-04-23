import shortuuid
from django.db import models
from django.contrib.auth.models import User

class ShortenedURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    user_name = models.CharField(max_length=50, default="Anonymous")
    original_url = models.URLField(max_length=100)
    short_url = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate_short_url():
        # Generate a unique short URL using shortuuid
        return shortuuid.ShortUUID().random(length=8)
