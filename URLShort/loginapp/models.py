import shortuuid
from django.db import models

class ShortenedURL(models.Model):
    original_url = models.URLField(max_length=100)
    short_url = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    custom_short_url = models.CharField(max_length=50, blank=True, null=True)

    @staticmethod
    def generate_short_url():
        # Generate a unique short URL using shortuuid
        return shortuuid.ShortUUID().random(length=8)
