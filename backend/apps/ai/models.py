from django.conf import settings
from django.db import models

from apps.clients.models import Client
from apps.core.models import BaseModel
from apps.properties.models import Property
from apps.sales.models import Deal


class VoiceNoteStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    PROCESSING = 'Processing', 'Processing'
    COMPLETED = 'Completed', 'Completed'
    FAILED = 'Failed', 'Failed'


class VoiceNote(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='voice_notes',
        on_delete=models.CASCADE
    )

    audio_file = models.FileField(upload_to='voice_notes/%Y/%m/')
    transcript = models.TextField(blank=True, default='')
    summary = models.TextField(blank=True, default='')
    action_items = models.JSONField(default=list, blank=True)

    client = models.ForeignKey(
        Client,
        related_name='voice_notes',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    deal = models.ForeignKey(
        Deal,
        related_name='voice_notes',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    property = models.ForeignKey(
        Property,
        related_name='voice_notes',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=VoiceNoteStatus.choices,
        default=VoiceNoteStatus.PENDING,
        db_index=True
    )
    error_message = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'voice_notes'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['client', 'status'])
        ]

    def __str__(self):
        return f'VoiceNote {self.public_id}'
