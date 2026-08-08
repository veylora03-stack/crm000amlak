from django.urls import path

from .views import VoiceNoteView

urlpatterns = [
    path('voice-notes/', VoiceNoteView.as_view(), name='voice-notes'),
]
