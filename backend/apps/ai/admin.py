from django.contrib import admin

from .models import VoiceNote


@admin.register(VoiceNote)
class VoiceNoteAdmin(admin.ModelAdmin):
    list_display = [
        'public_id',
        'user',
        'status',
        'client',
        'deal',
        'property',
        'created_at',
        'is_deleted'
    ]
    list_filter = [
        'status',
        'is_deleted'
    ]
    search_fields = [
        'transcript',
        'summary',
        'user__username',
        'client__full_name'
    ]
    readonly_fields = [
        'public_id',
        'created_at',
        'updated_at',
        'deleted_at'
    ]
