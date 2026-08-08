from django.contrib import admin

from .models import Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 0
    fields = [
        'image',
        'thumbnail',
        'alt_text',
        'sort_order',
        'is_primary',
        'is_deleted'
    ]
    readonly_fields = [
        'thumbnail'
    ]


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = [
        'code',
        'title',
        'property_type',
        'listing_type',
        'status',
        'publish_status',
        'price',
        'city',
        'assigned_agent',
        'created_at',
        'is_deleted'
    ]
    list_filter = [
        'status',
        'publish_status',
        'property_type',
        'listing_type',
        'city',
        'is_deleted'
    ]
    search_fields = [
        'code',
        'title',
        'address',
        'city',
        'district',
        'neighborhood'
    ]
    readonly_fields = [
        'public_id',
        'created_at',
        'updated_at',
        'deleted_at'
    ]
    inlines = [
        PropertyImageInline
    ]


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = [
        'public_id',
        'property',
        'sort_order',
        'is_primary',
        'created_at',
        'is_deleted'
    ]
    list_filter = [
        'is_primary',
        'is_deleted'
    ]
    search_fields = [
        'property__code',
        'property__title',
        'alt_text'
    ]
    readonly_fields = [
        'public_id',
        'created_at',
        'updated_at',
        'deleted_at'
    ]
