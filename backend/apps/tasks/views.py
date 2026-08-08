from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone

from apps.core.permissions import IsAgentOrAbove
from apps.core.responses import success_response
from apps.core.viewsets import StandardModelViewSet

from .models import Task
from .serializers import (
    TaskCreateSerializer,
    TaskSerializer,
    TaskUpdateSerializer
)


class TaskFilter(filters.FilterSet):
    due_date_from = filters.DateFilter(field_name='due_date', lookup_expr='gte')
    due_date_to = filters.DateFilter(field_name='due_date', lookup_expr='lte')

    class Meta:
        model = Task
        fields = ['assigned_user', 'client', 'deal', 'property', 'priority', 'status']


class TaskViewSet(StandardModelViewSet):
    queryset = Task.active_objects.all().select_related(
        'assigned_user', 'client', 'deal', 'property', 'created_by'
    )
    permission_classes = [IsAuthenticated, IsAgentOrAbove]
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at', 'priority', 'status']
    lookup_field = 'public_id'

    def get_serializer_class(self):
        if self.action == 'create':
            return TaskCreateSerializer
        if self.action in ['update', 'partial_update']:
            return TaskUpdateSerializer
        return TaskSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, public_id=None):
        task = self.get_object()
        task.status = 'Done'
        task.completed_at = timezone.now()
        task.save(update_fields=['status', 'completed_at', 'updated_at'])

        return Response(success_response(TaskSerializer(task).data))
