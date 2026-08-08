from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.permissions import IsAdmin
from apps.core.responses import success_response


class SettingsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        data = {
            'agency_name': 'CRM تخصصی املاک',
            'currency': 'IRR',
            'date_format': 'jalali',
            'language': 'fa',
            'direction': 'rtl'
        }

        return Response(success_response(data))

    def patch(self, request):
        return Response(success_response(request.data))
