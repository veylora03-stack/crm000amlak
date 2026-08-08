from django.conf import settings
from django.db import models

from apps.clients.models import Client
from apps.core.models import BaseModel


class PropertyStatus(models.TextChoices):
    DRAFT = 'Draft', 'Draft'
    PUBLISHED = 'Published', 'Published'
    RESERVED = 'Reserved', 'Reserved'
    SOLD = 'Sold', 'Sold'
    RENTED = 'Rented', 'Rented'
    EXPIRED = 'Expired', 'Expired'
    ARCHIVED = 'Archived', 'Archived'


class PublishStatus(models.TextChoices):
    DRAFT = 'Draft', 'Draft'
    PUBLISHED = 'Published', 'Published'
    ARCHIVED = 'Archived', 'Archived'


class Property(BaseModel):
    code = models.CharField(max_length=50, db_index=True)
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, allow_unicode=True, blank=True, default='')

    property_type = models.CharField(max_length=100, blank=True, default='', db_index=True)
    listing_type = models.CharField(max_length=100, blank=True, default='', db_index=True)

    status = models.CharField(
        max_length=20,
        choices=PropertyStatus.choices,
        default=PropertyStatus.DRAFT,
        db_index=True
    )
    publish_status = models.CharField(
        max_length=20,
        choices=PublishStatus.choices,
        default=PublishStatus.DRAFT,
        db_index=True
    )

    price = models.BigIntegerField(default=0)
    deposit_amount = models.BigIntegerField(default=0)
    rent_amount = models.BigIntegerField(default=0)

    land_area = models.PositiveIntegerField(default=0)
    building_area = models.PositiveIntegerField(default=0)

    bedrooms = models.PositiveSmallIntegerField(default=0)
    bathrooms = models.PositiveSmallIntegerField(default=0)
    parking_count = models.PositiveSmallIntegerField(default=0)

    floor_number = models.SmallIntegerField(blank=True, null=True)
    total_floors = models.SmallIntegerField(blank=True, null=True)
    year_built = models.PositiveSmallIntegerField(blank=True, null=True)

    address = models.TextField(blank=True, default='')
    province = models.CharField(max_length=100, blank=True, default='')
    city = models.CharField(max_length=100, blank=True, default='', db_index=True)
    district = models.CharField(max_length=100, blank=True, default='')
    neighborhood = models.CharField(max_length=100, blank=True, default='')

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True
    )
    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True
    )

    description = models.TextField(blank=True, default='')
    amenities = models.JSONField(default=list, blank=True)

    owner_client = models.ForeignKey(
        Client,
        related_name='owned_properties',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    assigned_agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='assigned_properties',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='created_properties',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='updated_properties',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'properties'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['code'],
                condition=models.Q(is_deleted=False),
                name='unique_active_property_code'
            )
        ]
        indexes = [
            models.Index(fields=['status', 'publish_status']),
            models.Index(fields=['property_type', 'listing_type']),
            models.Index(fields=['city', 'status']),
            models.Index(fields=['price']),
            models.Index(fields=['assigned_agent', 'status'])
        ]

    def __str__(self):
        return f'{self.code} - {self.title}'


class PropertyImage(BaseModel):
    property = models.ForeignKey(
        Property,
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='properties/%Y/%m/')
    thumbnail = models.ImageField(
        upload_to='properties/thumbnails/%Y/%m/',
        blank=True,
        null=True
    )
    alt_text = models.CharField(max_length=255, blank=True, default='')
    sort_order = models.PositiveIntegerField(default=0)
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = 'property_images'
        ordering = ['property', 'sort_order', 'created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['property', 'is_primary'],
                condition=models.Q(is_primary=True, is_deleted=False),
                name='unique_primary_image_per_property'
            )
        ]
        indexes = [
            models.Index(fields=['property', 'sort_order'])
        ]

    def __str__(self):
        return f'Image {self.public_id} for {self.property.code}'


class MatchScore(BaseModel):
    client = models.ForeignKey(
        Client,
        related_name='match_scores',
        on_delete=models.CASCADE
    )
    property = models.ForeignKey(
        Property,
        related_name='match_scores',
        on_delete=models.CASCADE
    )
    score = models.PositiveSmallIntegerField(default=0)
    matched_fields = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = 'match_scores'
        ordering = ['-score']
        constraints = [
            models.UniqueConstraint(
                fields=['client', 'property'],
                condition=models.Q(is_deleted=False),
                name='unique_active_client_property_match'
            )
        ]
        indexes = [
            models.Index(fields=['client', 'score']),
            models.Index(fields=['property', 'score'])
        ]

    def __str__(self):
        return f'Match {self.client.full_name} - {self.property.title}'
