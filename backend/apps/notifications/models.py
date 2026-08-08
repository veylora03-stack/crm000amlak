from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class Notification(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='notifications',
        on_delete=models.CASCADE
    )
    type = models.CharField(max_length=50, default='info', db_index=True)
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True, default='')
    payload = models.JSONField(default=dict, blank=True)

    is_read = models.BooleanField(default=False, db_index=True)
    read_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['user', 'created_at'])
        ]

    def __str__(self):
        return self.title
