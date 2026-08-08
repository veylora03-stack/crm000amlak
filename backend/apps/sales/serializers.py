from rest_framework import serializers

from .models import Deal, DealStatus, Pipeline, Stage


class PipelineSerializer(serializers.ModelSerializer):
    stages_count = serializers.SerializerMethodField()

    class Meta:
        model = Pipeline
        fields = [
            'public_id',
            'name',
            'description',
            'is_active',
            'sort_order',
            'stages_count',
            'created_at'
        ]
        read_only_fields = ['public_id', 'created_at']

    def get_stages_count(self, obj):
        return obj.stages.filter(is_deleted=False).count()


class StageSerializer(serializers.ModelSerializer):
    deals_count = serializers.SerializerMethodField()
    deals_total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Stage
        fields = [
            'public_id',
            'pipeline',
            'name',
            'color',
            'sort_order',
            'is_won_stage',
            'is_lost_stage',
            'deals_count',
            'deals_total_amount',
            'created_at'
        ]
        read_only_fields = ['public_id', 'created_at']

    def get_deals_count(self, obj):
        return obj.deals.filter(is_deleted=False).count()

    def get_deals_total_amount(self, obj):
        from django.db.models import Sum
        result = obj.deals.filter(is_deleted=False).aggregate(total=Sum('amount'))
        return result['total'] or 0


class DealSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.full_name', read_only=True, default='')
    property_title = serializers.CharField(source='property.title', read_only=True, default='')
    pipeline_name = serializers.CharField(source='pipeline.name', read_only=True, default='')
    stage_name = serializers.CharField(source='stage.name', read_only=True, default='')
    agent_name = serializers.CharField(source='agent.full_name', read_only=True, default='')

    class Meta:
        model = Deal
        fields = [
            'public_id',
            'title',
            'client',
            'client_name',
            'property',
            'property_title',
            'pipeline',
            'pipeline_name',
            'stage',
            'stage_name',
            'agent',
            'agent_name',
            'amount',
            'probability',
            'expected_close_date',
            'source',
            'status',
            'lost_reason',
            'won_reason',
            'notes',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['public_id', 'created_at', 'updated_at']


class DealCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = [
            'title',
            'client',
            'property',
            'pipeline',
            'stage',
            'agent',
            'amount',
            'probability',
            'expected_close_date',
            'source',
            'status',
            'lost_reason',
            'won_reason',
            'notes'
        ]

    def validate(self, attrs):
        amount = attrs.get('amount', 0)
        probability = attrs.get('probability', 0)

        if amount < 0:
            raise serializers.ValidationError('مبلغ معامله نمی‌تواند منفی باشد.')

        if probability < 0 or probability > 100:
            raise serializers.ValidationError('احتمال موفقیت باید بین 0 تا 100 باشد.')

        stage = attrs.get('stage')
        pipeline = attrs.get('pipeline')

        if stage and pipeline and stage.pipeline_id != pipeline.public_id:
            raise serializers.ValidationError('Stage انتخاب‌شده متعلق به Pipeline انتخاب‌شده نیست.')

        return attrs


class DealUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = [
            'title',
            'client',
            'property',
            'pipeline',
            'stage',
            'agent',
            'amount',
            'probability',
            'expected_close_date',
            'source',
            'status',
            'lost_reason',
            'won_reason',
            'notes'
        ]

    def validate(self, attrs):
        amount = attrs.get('amount', 0)
        probability = attrs.get('probability', 0)

        if amount < 0:
            raise serializers.ValidationError('مبلغ معامله نمی‌تواند منفی باشد.')

        if probability < 0 or probability > 100:
            raise serializers.ValidationError('احتمال موفقیت باید بین 0 تا 100 باشد.')

        return attrs


class DealMoveSerializer(serializers.Serializer):
    stage = serializers.UUIDField()

    def validate_stage(self, value):
        try:
            stage = Stage.active_objects.get(public_id=value)
        except Stage.DoesNotExist:
            raise serializers.ValidationError('Stage مورد نظر یافت نشد.')

        return stage
