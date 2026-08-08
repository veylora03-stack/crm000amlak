import uuid

from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='audit_logs',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    action = models.CharField(max_length=50, db_index=True)
    entity_name = models.CharField(max_length=100, db_index=True)
    entity_id = models.CharField(max_length=100, blank=True, default='')

    before_data = models.JSONField(blank=True, null=True)
    after_data = models.JSONField(blank=True, null=True)

    ip = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'audit_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['entity_name', 'entity_id']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['action', 'created_at'])
        ]

    def __str__(self):
        return f'{self.action} {self.entity_name} {self.entity_id}'
