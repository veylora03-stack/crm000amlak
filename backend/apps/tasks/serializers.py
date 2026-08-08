from rest_framework import serializers

from .models import Task, TaskPriority, TaskStatus


class TaskSerializer(serializers.ModelSerializer):
    assigned_user_name = serializers.CharField(source='assigned_user.full_name', read_only=True, default='')
    client_name = serializers.CharField(source='client.full_name', read_only=True, default='')
    deal_title = serializers.CharField(source='deal.title', read_only=True, default='')
    property_title = serializers.CharField(source='property.title', read_only=True, default='')

    class Meta:
        model = Task
        fields = [
            'public_id',
            'title',
            'description',
            'assigned_user',
            'assigned_user_name',
            'client',
            'client_name',
            'deal',
            'deal_title',
            'property',
            'property_title',
            'priority',
            'status',
            'due_date',
            'due_time',
            'completed_at',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['public_id', 'completed_at', 'created_at', 'updated_at']


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'assigned_user',
            'client',
            'deal',
            'property',
            'priority',
            'status',
            'due_date',
            'due_time'
        ]


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'assigned_user',
            'client',
            'deal',
            'property',
            'priority',
            'status',
            'due_date',
            'due_time'
        ]
