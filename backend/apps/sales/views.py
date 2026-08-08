from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.permissions import IsAgentOrAbove
from apps.core.responses import success_response
from apps.core.viewsets import StandardModelViewSet

from .models import Deal, Pipeline, Stage
from .serializers import (
    DealCreateSerializer,
    DealMoveSerializer,
    DealSerializer,
    DealUpdateSerializer,
    PipelineSerializer,
    StageSerializer
)


class PipelineViewSet(StandardModelViewSet):
    queryset = Pipeline.active_objects.all()
    serializer_class = PipelineSerializer
    permission_classes = [IsAuthenticated, IsAgentOrAbove]
    lookup_field = 'public_id'
    search_fields = ['name']
    ordering_fields = ['sort_order', 'created_at', 'name']


class StageViewSet(StandardModelViewSet):
    queryset = Stage.active_objects.all().select_related('pipeline')
    serializer_class = StageSerializer
    permission_classes = [IsAuthenticated, IsAgentOrAbove]
    lookup_field = 'public_id'
    filterset_fields = ['pipeline', 'is_won_stage', 'is_lost_stage']
    search_fields = ['name']
    ordering_fields = ['sort_order', 'created_at', 'name']


class DealFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_search')
    amount_min = filters.NumberFilter(field_name='amount', lookup_expr='gte')
    amount_max = filters.NumberFilter(field_name='amount', lookup_expr='lte')
    expected_close_date_from = filters.DateFilter(field_name='expected_close_date', lookup_expr='gte')
    expected_close_date_to = filters.DateFilter(field_name='expected_close_date', lookup_expr='lte')

    class Meta:
        model = Deal
        fields = ['pipeline', 'stage', 'agent', 'status', 'client', 'property']

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset

        from django.db.models import Q
        return queryset.filter(
            Q(title__icontains=value) |
            Q(client__full_name__icontains=value) |
            Q(property__title__icontains=value) |
            Q(notes__icontains=value)
        )


class DealViewSet(StandardModelViewSet):
    queryset = Deal.active_objects.all().select_related(
        'client', 'property', 'pipeline', 'stage', 'agent', 'created_by'
    )
    permission_classes = [IsAuthenticated, IsAgentOrAbove]
    filterset_class = DealFilter
    search_fields = ['title', 'client__full_name', 'property__title']
    ordering_fields = ['created_at', 'updated_at', 'amount', 'expected_close_date', 'title']
    lookup_field = 'public_id'

    def get_serializer_class(self):
        if self.action == 'create':
            return DealCreateSerializer
        if self.action in ['update', 'partial_update']:
            return DealUpdateSerializer
        return DealSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def move(self, request, public_id=None):
        deal = self.get_object()
        serializer = DealMoveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_stage = serializer.validated_data['stage']

        if new_stage.pipeline_id != deal.pipeline_id:
            return Response({
                'success': False,
                'data': None,
                'meta': None,
                'errors': [{'code': 'VALIDATION_ERROR', 'field': 'stage', 'message': 'Stage متعلق به Pipeline معامله نیست.'}]
            }, status=status.HTTP_400_BAD_REQUEST)

        old_stage = deal.stage
        deal.stage = new_stage
        deal.updated_by = request.user

        if new_stage.is_won_stage:
            deal.status = 'Won'
        elif new_stage.is_lost_stage:
            deal.status = 'Lost'
        else:
            deal.status = 'Open'

        deal.save(update_fields=['stage', 'status', 'updated_by', 'updated_at'])

        return Response(success_response(DealSerializer(deal).data))
