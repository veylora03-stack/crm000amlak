from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import NotificationViewSet

router = DefaultRouter()
router.register('', NotificationViewSet, basename='notifications')

urlpatterns = [
    path('read-all/', NotificationViewSet.as_view({'post': 'read_all'}), name='notification-read-all'),
] + router.urls
