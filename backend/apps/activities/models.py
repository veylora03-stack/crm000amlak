from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.clients.models import Client
from apps.core.models import BaseModel
from apps.properties.models import Property
from apps.sales.models import Deal


class InteractionType(models.TextChoices):
    CALL = 'call', 'call'
    MEETING = 'meeting', 'meeting'
    EMAIL = 'email', 'email'
    MESSAGE = 'message', 'message'
    NOTE = 'note', 'note'
    VISIT = 'visit', 'visit'
    FILE = 'file', 'file'
    OTHER = 'other', 'other'


class Interaction(BaseModel):
    interaction_type = models.CharField(
        max_length=20,
        choices=InteractionType.choices,
        default=InteractionType.CALL,
        db_index=True
    )

    client = models.ForeignKey(
        Client,
        related_name='interactions',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    deal = models.ForeignKey(
        Deal,
        related_name='interactions',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    property = models.ForeignKey(
        Property,
        related_name='interactions',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='interactions',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    title = models.CharField(max_length=255, blank=True, default='')
    body = models.TextField(blank=True, default='')

    occurred_at = models.DateTimeField(default=timezone.now, db_index=True)
    duration_minutes = models.PositiveIntegerField(default=0)

    needs_followup = models.BooleanField(default=False, db_index=True)
    followup_at = models.DateTimeField(blank=True, null=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='created_interactions',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'interactions'
        ordering = ['-occurred_at']
        indexes = [
            models.Index(fields=['client', 'occurred_at']),
            models.Index(fields=['deal', 'occurred_at']),
            models.Index(fields=['needs_followup', 'followup_at'])
        ]

    def __str__(self):
        return self.title or self.interaction_type
