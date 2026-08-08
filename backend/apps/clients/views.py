from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.permissions import IsAgentOrAbove
from apps.core.responses import success_response
from apps.core.viewsets import StandardModelViewSet

from .models import Client
from .serializers import (
    ClientCreateSerializer,
    ClientListSerializer,
    ClientSerializer,
    ClientUpdateSerializer
)


class ClientFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_search')
    date_from = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Client
        fields = ['status', 'customer_type', 'source', 'assigned_agent']

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset

        from django.db.models import Q
        return queryset.filter(
            Q(full_name__icontains=value) |
            Q(phone__icontains=value) |
            Q(email__icontains=value) |
            Q(notes__icontains=value)
        )


class ClientViewSet(StandardModelViewSet):
    queryset = Client.active_objects.all().select_related('assigned_agent', 'created_by')
    permission_classes = [IsAuthenticated, IsAgentOrAbove]
    filterset_class = ClientFilter
    search_fields = ['full_name', 'phone', 'email']
    ordering_fields = ['created_at', 'updated_at', 'full_name', 'score']
    lookup_field = 'public_id'

    def get_serializer_class(self):
        if self.action == 'create':
            return ClientCreateSerializer
        if self.action in ['update', 'partial_update']:
            return ClientUpdateSerializer
        if self.action == 'list':
            return ClientListSerializer
        return ClientSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    @action(detail=True, methods=['get'])
    def timeline(self, request, public_id=None):
        client = self.get_object()
        interactions = client.interactions.filter(is_deleted=False).order_by('-occurred_at')[:20]

        from apps.activities.serializers import InteractionSerializer
        data = InteractionSerializer(interactions, many=True).data

        return Response(success_response(data))

    @action(detail=True, methods=['get'])
    def deals(self, request, public_id=None):
        client = self.get_object()
        deals = client.deals.filter(is_deleted=False).order_by('-created_at')

        from apps.sales.serializers import DealListSerializer
        data = DealListSerializer(deals, many=True).data

        return Response(success_response(data))

    @action(detail=True, methods=['get'])
    def interactions(self, request, public_id=None):
        client = self.get_object()
        interactions = client.interactions.filter(is_deleted=False).order_by('-occurred_at')

        from apps.activities.serializers import InteractionSerializer
        data = InteractionSerializer(interactions, many=True).data

        return Response(success_response(data))

    @action(detail=True, methods=['post'])
    def assign(self, request, public_id=None):
        client = self.get_object()
        agent_id = request.data.get('assigned_agent')

        if not agent_id:
            return Response({
                'success': False,
                'data': None,
                'meta': None,
                'errors': [{'code': 'VALIDATION_ERROR', 'field': 'assigned_agent', 'message': 'Agent الزامی است.'}]
            }, status=status.HTTP_400_BAD_REQUEST)

        from django.contrib.auth import get_user_model
        User = get_user_model()

        try:
            agent = User.active_objects.get(public_id=agent_id)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'data': None,
                'meta': None,
                'errors': [{'code': 'NOT_FOUND', 'field': 'assigned_agent', 'message': 'Agent مورد نظر یافت نشد.'}]
            }, status=status.HTTP_404_NOT_FOUND)

        client.assigned_agent = agent
        client.updated_by = request.user
        client.save(update_fields=['assigned_agent', 'updated_by', 'updated_at'])

        return Response(success_response(ClientSerializer(client).data))
