from django.contrib import admin

from .models import Deal, Pipeline, Stage


class StageInline(admin.TabularInline):
    model = Stage
    extra = 0
    fields = [
        'name',
        'color',
        'sort_order',
        'is_won_stage',
        'is_lost_stage',
        'is_deleted'
    ]


@admin.register(Pipeline)
class PipelineAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'is_active',
        'sort_order',
        'created_at',
        'is_deleted'
    ]
    list_filter = [
        'is_active',
        'is_deleted'
    ]
    search_fields = [
        'name',
        'description'
    ]
    inlines = [
        StageInline
    ]
    readonly_fields = [
        'public_id',
        'created_at',
        'updated_at',
        'deleted_at'
    ]


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'pipeline',
        'sort_order',
        'is_won_stage',
        'is_lost_stage',
        'is_deleted'
    ]
    list_filter = [
        'pipeline',
        'is_won_stage',
        'is_lost_stage',
        'is_deleted'
    ]
    search_fields = [
        'name',
        'pipeline__name'
    ]
    readonly_fields = [
        'public_id',
        'created_at',
        'updated_at',
        'deleted_at'
    ]


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'client',
        'pipeline',
        'stage',
        'agent',
        'amount',
        'status',
        'expected_close_date',
        'is_deleted'
    ]
    list_filter = [
        'status',
        'pipeline',
        'stage',
        'is_deleted'
    ]
    search_fields = [
        'title',
        'client__full_name',
        'property__title',
        'notes'
    ]
    readonly_fields = [
        'public_id',
        'created_at',
        'updated_at',
        'deleted_at'
    ]
