import shortuuid
from django.db import models

class ShortenedURL(models.Model):
    original_url = models.URLField(max_length=200)
    short_url = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.short_url:
            # Generate a unique short URL using shortuuid
            self.short_url = shortuuid.ShortUUID().random(length=8)
        super().save(*args, **kwargs)

