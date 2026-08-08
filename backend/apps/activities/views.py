from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated

from apps.core.permissions import IsAgentOrAbove
from apps.core.viewsets import StandardModelViewSet

from .models import Interaction
from .serializers import (
    InteractionCreateSerializer,
    InteractionSerializer,
    InteractionUpdateSerializer
)


class InteractionFilter(filters.FilterSet):
    date_from = filters.DateFilter(field_name='occurred_at', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='occurred_at', lookup_expr='lte')

    class Meta:
        model = Interaction
        fields = ['interaction_type', 'client', 'deal', 'property', 'agent', 'needs_followup']


class InteractionViewSet(StandardModelViewSet):
    queryset = Interaction.active_objects.all().select_related(
        'client', 'deal', 'property', 'agent'
    )
    permission_classes = [IsAuthenticated, IsAgentOrAbove]
    filterset_class = InteractionFilter
    search_fields = ['title', 'body']
    ordering_fields = ['occurred_at', 'created_at']
    lookup_field = 'public_id'

    def get_serializer_class(self):
        if self.action == 'create':
            return InteractionCreateSerializer
        if self.action in ['update', 'partial_update']:
            return InteractionUpdateSerializer
        return InteractionSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
