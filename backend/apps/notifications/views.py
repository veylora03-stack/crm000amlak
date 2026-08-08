from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone

from apps.core.responses import success_response
from apps.core.viewsets import StandardModelViewSet

from .models import Notification
from .serializers import NotificationSerializer


class NotificationFilter(filters.FilterSet):
    class Meta:
        model = Notification
        fields = ['type', 'is_read']


class NotificationViewSet(StandardModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = NotificationFilter
    ordering_fields = ['created_at']
    lookup_field = 'public_id'
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return Notification.active_objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def read(self, request, public_id=None):
        notification = self.get_object()
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save(update_fields=['is_read', 'read_at', 'updated_at'])

        return Response(success_response(NotificationSerializer(notification).data))

    @action(detail=False, methods=['post'])
    def read_all(self, request):
        updated_count = self.get_queryset().filter(is_read=False).update(
            is_read=True,
            read_at=timezone.now()
        )

        return Response(success_response({'updated_count': updated_count}))
