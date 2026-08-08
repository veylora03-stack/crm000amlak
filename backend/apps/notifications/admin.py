from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'user',
        'type',
        'is_read',
        'read_at',
        'created_at',
        'is_deleted'
    ]
    list_filter = [
        'type',
        'is_read',
        'is_deleted'
    ]
    search_fields = [
        'title',
        'body',
        'user__username'
    ]
    readonly_fields = [
        'public_id',
        'created_at',
        'updated_at',
        'deleted_at'
    ]
