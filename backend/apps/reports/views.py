from django.db.models import Count, Sum, Q
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
import csv
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.clients.models import Client
from apps.sales.models import Deal, Stage
from apps.properties.models import Property
from apps.tasks.models import Task
from apps.activities.models import Interaction
from apps.core.responses import success_response


class ReportLeadsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        status_filter = request.query_params.get('status')
        source_filter = request.query_params.get('source')

        queryset = Client.active_objects.all()

        if date_from:
            queryset = queryset.filter(created_at__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__date__lte=date_to)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if source_filter:
            queryset = queryset.filter(source=source_filter)

        from apps.clients.serializers import ClientListSerializer
        data = ClientListSerializer(queryset.order_by('-created_at')[:1000], many=True).data

        return Response(success_response(data))


class ReportDealsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        status_filter = request.query_params.get('status')
        agent_filter = request.query_params.get('agent')

        queryset = Deal.active_objects.all().select_related('client', 'property', 'stage', 'agent')

        if date_from:
            queryset = queryset.filter(created_at__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__date__lte=date_to)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if agent_filter:
            queryset = queryset.filter(agent__public_id=agent_filter)

        from apps.sales.serializers import DealSerializer
        data = DealSerializer(queryset.order_by('-created_at')[:1000], many=True).data

        return Response(success_response(data))


class ReportAgentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        agents = User.active_objects.filter(role__in=['Agent', 'Manager', 'Admin'])

        report = []
        for agent in agents:
            deals = Deal.active_objects.filter(agent=agent)
            won_deals = deals.filter(status='Won')
            lost_deals = deals.filter(status='Lost')

            report.append({
                'agent': {
                    'public_id': str(agent.public_id),
                    'full_name': agent.full_name,
                    'role': agent.role
                },
                'total_deals': deals.count(),
                'won_deals': won_deals.count(),
                'lost_deals': lost_deals.count(),
                'total_amount': deals.aggregate(total=Sum('amount'))['total'] or 0,
                'won_amount': won_deals.aggregate(total=Sum('amount'))['total'] or 0
            })

        return Response(success_response(report))


class ReportFunnelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pipeline_id = request.query_params.get('pipeline')

        stages = Stage.active_objects.all().order_by('sort_order')
        if pipeline_id:
            stages = stages.filter(pipeline__public_id=pipeline_id)

        funnel = []
        for stage in stages:
            deals_count = stage.deals.filter(is_deleted=False).count()
            deals_amount = stage.deals.filter(is_deleted=False).aggregate(total=Sum('amount'))['total'] or 0

            funnel.append({
                'stage': {
                    'public_id': str(stage.public_id),
                    'name': stage.name,
                    'color': stage.color,
                    'sort_order': stage.sort_order
                },
                'deals_count': deals_count,
                'deals_amount': deals_amount
            })

        return Response(success_response(funnel))


class ReportPropertiesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        status_filter = request.query_params.get('status')
        property_type = request.query_params.get('property_type')

        queryset = Property.active_objects.all()

        if date_from:
            queryset = queryset.filter(created_at__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__date__lte=date_to)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if property_type:
            queryset = queryset.filter(property_type=property_type)

        from apps.properties.serializers import PropertyListSerializer
        data = PropertyListSerializer(queryset.order_by('-created_at')[:1000], many=True).data

        return Response(success_response(data))


class ReportExportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        report_type = request.query_params.get('report_type', 'leads')
        export_format = request.query_params.get('format', 'csv')

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{report_type}_report.csv"'
        response.write('\ufeff')

        writer = csv.writer(response)

        if report_type == 'leads':
            writer.writerow(['نام', 'موبایل', 'ایمیل', 'وضعیت', 'نوع مشتری', 'منبع', 'تاریخ ایجاد'])
            for client in Client.active_objects.all()[:1000]:
                writer.writerow([
                    client.full_name,
                    client.phone,
                    client.email,
                    client.status,
                    client.customer_type,
                    client.source,
                    client.created_at.strftime('%Y-%m-%d %H:%M')
                ])

        elif report_type == 'deals':
            writer.writerow(['عنوان', 'مشتری', 'ملک', 'Stage', 'مبلغ', 'وضعیت', 'تاریخ ایجاد'])
            for deal in Deal.active_objects.all().select_related('client', 'property', 'stage')[:1000]:
                writer.writerow([
                    deal.title,
                    deal.client.full_name if deal.client else '',
                    deal.property.title if deal.property else '',
                    deal.stage.name,
                    deal.amount,
                    deal.status,
                    deal.created_at.strftime('%Y-%m-%d %H:%M')
                ])

        elif report_type == 'properties':
            writer.writerow(['کد', 'عنوان', 'نوع', 'وضعیت', 'قیمت', 'شهر', 'تاریخ ایجاد'])
            for property_obj in Property.active_objects.all()[:1000]:
                writer.writerow([
                    property_obj.code,
                    property_obj.title,
                    property_obj.property_type,
                    property_obj.status,
                    property_obj.price,
                    property_obj.city,
                    property_obj.created_at.strftime('%Y-%m-%d %H:%M')
                ])

        return response
