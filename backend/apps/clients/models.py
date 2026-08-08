from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class ClientStatus(models.TextChoices):
    NEW = 'New', 'New'
    CONTACTED = 'Contacted', 'Contacted'
    QUALIFIED = 'Qualified', 'Qualified'
    UNQUALIFIED = 'Unqualified', 'Unqualified'
    NEGOTIATING = 'Negotiating', 'Negotiating'
    WON = 'Won', 'Won'
    LOST = 'Lost', 'Lost'
    ARCHIVED = 'Archived', 'Archived'


class Client(BaseModel):
    full_name = models.CharField(max_length=255, db_index=True)
    phone = models.CharField(max_length=20, db_index=True)
    email = models.EmailField(blank=True, default='', db_index=True)
    source = models.CharField(max_length=100, blank=True, default='')
    status = models.CharField(
        max_length=20,
        choices=ClientStatus.choices,
        default=ClientStatus.NEW,
        db_index=True
    )
    customer_type = models.CharField(max_length=100, blank=True, default='')
    budget_min = models.BigIntegerField(default=0)
    budget_max = models.BigIntegerField(default=0)
    preferred_areas = models.JSONField(default=list, blank=True)
    preferred_property_types = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True, default='')
    score = models.PositiveIntegerField(default=0)

    assigned_agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='assigned_clients',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='created_clients',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='updated_clients',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'clients'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['phone'],
                condition=models.Q(is_deleted=False) & ~models.Q(phone=''),
                name='unique_active_client_phone'
            )
        ]
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['assigned_agent', 'status']),
            models.Index(fields=['customer_type', 'status'])
        ]

    def __str__(self):
        return self.full_name
