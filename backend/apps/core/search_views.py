from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.clients.models import Client
from apps.properties.models import Property
from apps.sales.models import Deal
from apps.tasks.models import Task
from apps.core.responses import success_response


class GlobalSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q', '').strip()

        if not query:
            return Response(success_response({
                'clients': [],
                'properties': [],
                'deals': [],
                'tasks': []
            }))

        clients = Client.active_objects.filter(
            Q(full_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query)
        )[:5]

        properties = Property.active_objects.filter(
            Q(code__icontains=query) |
            Q(title__icontains=query) |
            Q(address__icontains=query) |
            Q(city__icontains=query)
        )[:5]

        deals = Deal.active_objects.filter(
            Q(title__icontains=query) |
            Q(client__full_name__icontains=query) |
            Q(property__title__icontains=query)
        )[:5]

        tasks = Task.active_objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )[:5]

        data = {
            'clients': [{
                'public_id': str(c.public_id),
                'full_name': c.full_name,
                'phone': c.phone
            } for c in clients],
            'properties': [{
                'public_id': str(p.public_id),
                'code': p.code,
                'title': p.title,
                'city': p.city
            } for p in properties],
            'deals': [{
                'public_id': str(d.public_id),
                'title': d.title,
                'client_name': d.client.full_name if d.client else None
            } for d in deals],
            'tasks': [{
                'public_id': str(t.public_id),
                'title': t.title,
                'status': t.status
            } for t in tasks]
        }

        return Response(success_response(data))
