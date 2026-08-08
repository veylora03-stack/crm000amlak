from django.contrib import admin

from .models import Interaction


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'interaction_type',
        'client',
        'deal',
        'property',
        'agent',
        'occurred_at',
        'needs_followup',
        'is_deleted'
    ]
    list_filter = [
        'interaction_type',
        'needs_followup',
        'is_deleted'
    ]
    search_fields = [
        'title',
        'body',
        'client__full_name',
        'deal__title',
        'property__title'
    ]
    readonly_fields = [
        'public_id',
        'created_at',
        'updated_at',
        'deleted_at'
    ]
