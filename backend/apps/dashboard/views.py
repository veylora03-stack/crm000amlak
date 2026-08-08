from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.clients.models import Client
from apps.sales.models import Deal, Stage
from apps.properties.models import Property
from apps.tasks.models import Task
from apps.core.responses import success_response


class DashboardKpisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_ago = now - timedelta(days=7)
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        leads_today = Client.active_objects.filter(created_at__gte=today_start).count()
        leads_week = Client.active_objects.filter(created_at__gte=week_ago).count()

        active_deals = Deal.active_objects.filter(status='Open')
        active_deals_count = active_deals.count()
        active_deals_value = active_deals.aggregate(total=Sum('amount'))['total'] or 0

        visits_registered = Client.active_objects.filter(
            interactions__interaction_type='visit',
            interactions__is_deleted=False
        ).distinct().count()

        won_month = Deal.active_objects.filter(
            status='Won',
            updated_at__gte=month_start
        ).count()

        lost_month = Deal.active_objects.filter(
            status='Lost',
            updated_at__gte=month_start
        ).count()

        total_leads = Client.active_objects.count()
        total_deals = Deal.active_objects.count()
        conversion_rate = round((total_deals / total_leads * 100), 2) if total_leads > 0 else 0

        tasks_today = Task.active_objects.filter(
            due_date=now.date(),
            status__in=['Todo', 'In Progress']
        ).count()

        overdue_tasks = Task.active_objects.filter(
            due_date__lt=now.date(),
            status__in=['Todo', 'In Progress']
        ).count()

        active_properties = Property.active_objects.filter(publish_status='Published').count()
        sold_properties = Property.active_objects.filter(status='Sold').count()
        rented_properties = Property.active_objects.filter(status='Rented').count()

        data = {
            'leads_today': leads_today,
            'leads_week': leads_week,
            'active_deals': active_deals_count,
            'active_deals_value': active_deals_value,
            'visits_registered': visits_registered,
            'won_month': won_month,
            'lost_month': lost_month,
            'conversion_rate': conversion_rate,
            'tasks_today': tasks_today,
            'overdue_tasks': overdue_tasks,
            'active_properties': active_properties,
            'sold_properties': sold_properties,
            'rented_properties': rented_properties
        }

        return Response(success_response(data))


class DashboardChartsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()

        leads_by_month = Client.active_objects.filter(
            created_at__gte=now - timedelta(days=180)
        ).extra(
            select={'month': "TO_CHAR(created_at, 'YYYY-MM')"}
        ).values('month').annotate(count=Count('id')).order_by('month')

        deals_by_stage = Deal.active_objects.filter(status='Open').values(
            'stage__name'
        ).annotate(count=Count('id'), total=Sum('amount')).order_by('stage__sort_order')

        data = {
            'leads_by_month': list(leads_by_month),
            'deals_by_stage': list(deals_by_stage)
        }

        return Response(success_response(data))


class DashboardRecentActivitiesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from apps.activities.models import Interaction
        from apps.activities.serializers import InteractionSerializer

        recent_interactions = Interaction.active_objects.all().select_related(
            'client', 'deal', 'property', 'agent'
        ).order_by('-occurred_at')[:10]

        data = InteractionSerializer(recent_interactions, many=True).data

        return Response(success_response(data))
