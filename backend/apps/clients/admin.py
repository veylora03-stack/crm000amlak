from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [
        'full_name',
        'phone',
        'status',
        'customer_type',
        'assigned_agent',
        'created_at',
        'is_deleted'
    ]
    list_filter = [
        'status',
        'customer_type',
        'source',
        'is_deleted'
    ]
    search_fields = [
        'full_name',
        'phone',
        'email',
        'notes'
    ]
    readonly_fields = [
        'public_id',
        'created_at',
        'updated_at',
        'deleted_at'
    ]
