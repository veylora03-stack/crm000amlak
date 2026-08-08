from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.permissions import IsAgentOrAbove
from apps.core.responses import success_response

from .models import VoiceNote


class VoiceNoteView(APIView):
    permission_classes = [IsAuthenticated, IsAgentOrAbove]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        audio_file = request.FILES.get('audio')

        if not audio_file:
            return Response({
                'success': False,
                'data': None,
                'meta': None,
                'errors': [{'code': 'VALIDATION_ERROR', 'field': 'audio', 'message': 'فایل صوتی الزامی است.'}]
            }, status=status.HTTP_400_BAD_REQUEST)

        voice_note = VoiceNote.objects.create(
            user=request.user,
            audio_file=audio_file,
            status='Pending'
        )

        data = {
            'public_id': str(voice_note.public_id),
            'status': voice_note.status,
            'created_at': voice_note.created_at.isoformat()
        }

        return Response(success_response(data), status=status.HTTP_201_CREATED)

    def get(self, request):
        voice_notes = VoiceNote.objects.filter(user=request.user).order_by('-created_at')[:20]

        data = [{
            'public_id': str(vn.public_id),
            'status': vn.status,
            'transcript': vn.transcript,
            'summary': vn.summary,
            'action_items': vn.action_items,
            'created_at': vn.created_at.isoformat()
        } for vn in voice_notes]

        return Response(success_response(data))
