from rest_framework import serializers

from .models import Interaction, InteractionType


class InteractionSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.full_name', read_only=True, default='')
    deal_title = serializers.CharField(source='deal.title', read_only=True, default='')
    property_title = serializers.CharField(source='property.title', read_only=True, default='')
    agent_name = serializers.CharField(source='agent.full_name', read_only=True, default='')

    class Meta:
        model = Interaction
        fields = [
            'public_id',
            'interaction_type',
            'client',
            'client_name',
            'deal',
            'deal_title',
            'property',
            'property_title',
            'agent',
            'agent_name',
            'title',
            'body',
            'occurred_at',
            'duration_minutes',
            'needs_followup',
            'followup_at',
            'created_at'
        ]
        read_only_fields = ['public_id', 'created_at']


class InteractionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = [
            'interaction_type',
            'client',
            'deal',
            'property',
            'agent',
            'title',
            'body',
            'occurred_at',
            'duration_minutes',
            'needs_followup',
            'followup_at'
        ]

    def validate(self, attrs):
        client = attrs.get('client')
        deal = attrs.get('deal')
        property_obj = attrs.get('property')

        if not client and not deal and not property_obj:
            raise serializers.ValidationError('حداقل یکی از مشتری، معامله یا ملک باید مرتبط باشد.')

        return attrs


class InteractionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = [
            'interaction_type',
            'client',
            'deal',
            'property',
            'agent',
            'title',
            'body',
            'occurred_at',
            'duration_minutes',
            'needs_followup',
            'followup_at'
        ]
