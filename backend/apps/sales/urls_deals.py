from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import DealViewSet

router = DefaultRouter()
router.register('', DealViewSet, basename='deals')

urlpatterns = [
    path('<uuid:public_id>/move/', DealViewSet.as_view({'post': 'move'}), name='deal-move'),
] + router.urls
