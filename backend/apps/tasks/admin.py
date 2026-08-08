from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'assigned_user',
        'priority',
        'status',
        'due_date',
        'due_time',
        'completed_at',
        'is_deleted'
    ]
    list_filter = [
        'priority',
        'status',
        'is_deleted'
    ]
    search_fields = [
        'title',
        'description',
        'assigned_user__username',
        'client__full_name',
        'deal__title'
    ]
    readonly_fields = [
        'public_id',
        'created_at',
        'updated_at',
        'deleted_at'
    ]
