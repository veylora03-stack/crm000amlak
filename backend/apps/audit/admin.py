from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = [
        'action',
        'entity_name',
        'entity_id',
        'user',
        'ip',
        'created_at'
    ]
    list_filter = [
        'action',
        'entity_name'
    ]
    search_fields = [
        'entity_name',
        'entity_id',
        'user__username',
        'ip'
    ]
    readonly_fields = [
        'public_id',
        'created_at'
    ]
