from rest_framework import serializers

from .models import Client, ClientStatus


class ClientSerializer(serializers.ModelSerializer):
    assigned_agent_name = serializers.CharField(source='assigned_agent.full_name', read_only=True, default='')
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True, default='')

    class Meta:
        model = Client
        fields = [
            'public_id',
            'full_name',
            'phone',
            'email',
            'source',
            'status',
            'customer_type',
            'budget_min',
            'budget_max',
            'preferred_areas',
            'preferred_property_types',
            'notes',
            'score',
            'assigned_agent',
            'assigned_agent_name',
            'created_by',
            'created_by_name',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['public_id', 'created_at', 'updated_at']


class ClientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'full_name',
            'phone',
            'email',
            'source',
            'status',
            'customer_type',
            'budget_min',
            'budget_max',
            'preferred_areas',
            'preferred_property_types',
            'notes',
            'score',
            'assigned_agent'
        ]

    def validate_phone(self, value):
        if not value:
            raise serializers.ValidationError('شماره موبایل الزامی است.')

        if not value.isdigit():
            raise serializers.ValidationError('شماره موبایل معتبر نیست.')

        if len(value) != 11:
            raise serializers.ValidationError('شماره موبایل معتبر نیست.')

        if not value.startswith('09'):
            raise serializers.ValidationError('شماره موبایل معتبر نیست.')

        return value

    def validate(self, attrs):
        budget_min = attrs.get('budget_min', 0)
        budget_max = attrs.get('budget_max', 0)

        if budget_min < 0 or budget_max < 0:
            raise serializers.ValidationError('مبلغ بودجه نمی‌تواند منفی باشد.')

        if budget_min > budget_max:
            raise serializers.ValidationError('بودجه حداقل نمی‌تواند بیشتر از بودجه حداکثر باشد.')

        return attrs


class ClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'full_name',
            'phone',
            'email',
            'source',
            'status',
            'customer_type',
            'budget_min',
            'budget_max',
            'preferred_areas',
            'preferred_property_types',
            'notes',
            'score',
            'assigned_agent'
        ]

    def validate_phone(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError('شماره موبایل معتبر نیست.')

        if value and len(value) != 11:
            raise serializers.ValidationError('شماره موبایل معتبر نیست.')

        if value and not value.startswith('09'):
            raise serializers.ValidationError('شماره موبایل معتبر نیست.')

        return value

    def validate(self, attrs):
        budget_min = attrs.get('budget_min', 0)
        budget_max = attrs.get('budget_max', 0)

        if budget_min < 0 or budget_max < 0:
            raise serializers.ValidationError('مبلغ بودجه نمی‌تواند منفی باشد.')

        if budget_min > budget_max:
            raise serializers.ValidationError('بودجه حداقل نمی‌تواند بیشتر از بودجه حداکثر باشد.')

        return attrs


class ClientListSerializer(serializers.ModelSerializer):
    assigned_agent_name = serializers.CharField(source='assigned_agent.full_name', read_only=True, default='')

    class Meta:
        model = Client
        fields = [
            'public_id',
            'full_name',
            'phone',
            'email',
            'status',
            'customer_type',
            'source',
            'budget_min',
            'budget_max',
            'assigned_agent_name',
            'created_at'
        ]
