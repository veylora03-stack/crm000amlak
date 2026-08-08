from django.conf import settings
from django.db import models

from apps.clients.models import Client
from apps.core.models import BaseModel
from apps.properties.models import Property
from apps.sales.models import Deal


class TaskPriority(models.TextChoices):
    LOW = 'Low', 'Low'
    MEDIUM = 'Medium', 'Medium'
    HIGH = 'High', 'High'
    URGENT = 'Urgent', 'Urgent'


class TaskStatus(models.TextChoices):
    TODO = 'Todo', 'Todo'
    IN_PROGRESS = 'In Progress', 'In Progress'
    DONE = 'Done', 'Done'
    CANCELLED = 'Cancelled', 'Cancelled'


class Task(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')

    assigned_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='tasks',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    client = models.ForeignKey(
        Client,
        related_name='tasks',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    deal = models.ForeignKey(
        Deal,
        related_name='tasks',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    property = models.ForeignKey(
        Property,
        related_name='tasks',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    priority = models.CharField(
        max_length=10,
        choices=TaskPriority.choices,
        default=TaskPriority.MEDIUM,
        db_index=True
    )
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.TODO,
        db_index=True
    )

    due_date = models.DateField(blank=True, null=True, db_index=True)
    due_time = models.TimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='created_tasks',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'tasks'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['assigned_user', 'status']),
            models.Index(fields=['due_date', 'status']),
            models.Index(fields=['priority', 'status'])
        ]

    def __str__(self):
        return self.title
