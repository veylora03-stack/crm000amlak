from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.clients.models import Client
from apps.core.models import BaseModel
from apps.properties.models import Property


class Pipeline(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True, db_index=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'pipelines'
        ordering = ['sort_order', 'created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                condition=models.Q(is_active=True, is_deleted=False),
                name='unique_active_pipeline_name'
            )
        ]

    def __str__(self):
        return self.name


class Stage(BaseModel):
    pipeline = models.ForeignKey(
        Pipeline,
        related_name='stages',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=20, default='#3b82f6')
    sort_order = models.PositiveIntegerField(default=0)
    is_won_stage = models.BooleanField(default=False)
    is_lost_stage = models.BooleanField(default=False)

    class Meta:
        db_table = 'stages'
        ordering = ['pipeline', 'sort_order']
        constraints = [
            models.UniqueConstraint(
                fields=['pipeline', 'sort_order'],
                condition=models.Q(is_deleted=False),
                name='unique_active_stage_order_per_pipeline'
            ),
            models.UniqueConstraint(
                fields=['pipeline', 'name'],
                condition=models.Q(is_deleted=False),
                name='unique_active_stage_name_per_pipeline'
            )
        ]
        indexes = [
            models.Index(fields=['pipeline', 'sort_order'])
        ]

    def __str__(self):
        return f'{self.pipeline.name} - {self.name}'


class DealStatus(models.TextChoices):
    OPEN = 'Open', 'Open'
    WON = 'Won', 'Won'
    LOST = 'Lost', 'Lost'


class Deal(BaseModel):
    title = models.CharField(max_length=255)

    client = models.ForeignKey(
        Client,
        related_name='deals',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    property = models.ForeignKey(
        Property,
        related_name='deals',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    pipeline = models.ForeignKey(
        Pipeline,
        related_name='deals',
        on_delete=models.PROTECT
    )
    stage = models.ForeignKey(
        Stage,
        related_name='deals',
        on_delete=models.PROTECT
    )
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='deals',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    amount = models.BigIntegerField(default=0)
    probability = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    expected_close_date = models.DateField(blank=True, null=True, db_index=True)

    source = models.CharField(max_length=100, blank=True, default='')
    status = models.CharField(
        max_length=10,
        choices=DealStatus.choices,
        default=DealStatus.OPEN,
        db_index=True
    )

    lost_reason = models.CharField(max_length=255, blank=True, default='')
    won_reason = models.CharField(max_length=255, blank=True, default='')
    notes = models.TextField(blank=True, default='')

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='created_deals',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='updated_deals',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'deals'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['pipeline', 'stage']),
            models.Index(fields=['agent', 'status']),
            models.Index(fields=['expected_close_date', 'status']),
            models.Index(fields=['client', 'status'])
        ]

    def __str__(self):
        return self.title
