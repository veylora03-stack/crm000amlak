from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.core.permissions import IsAdmin
from apps.core.responses import success_response
from apps.core.pagination import StandardPagination

from .models import AuditLog


class AuditLogFilter(filters.FilterSet):
    date_from = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = AuditLog
        fields = ['action', 'entity_name', 'user']


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all().select_related('user')
    permission_classes = [IsAuthenticated, IsAdmin]
    pagination_class = StandardPagination
    filterset_class = AuditLogFilter
    search_fields = ['entity_name', 'entity_id', 'action']
    ordering_fields = ['created_at']
    lookup_field = 'public_id'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            data = [{
                'public_id': str(log.public_id),
                'user': log.user.full_name if log.user else None,
                'action': log.action,
                'entity_name': log.entity_name,
                'entity_id': log.entity_id,
                'before_data': log.before_data,
                'after_data': log.after_data,
                'ip': log.ip,
                'created_at': log.created_at.isoformat()
            } for log in page]
            return self.get_paginated_response(data)

        data = [{
            'public_id': str(log.public_id),
            'user': log.user.full_name if log.user else None,
            'action': log.action,
            'entity_name': log.entity_name,
            'entity_id': log.entity_id,
            'before_data': log.before_data,
            'after_data': log.after_data,
            'ip': log.ip,
            'created_at': log.created_at.isoformat()
        } for log in queryset]

        from rest_framework.response import Response
        return Response(success_response(data))
