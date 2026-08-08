from rest_framework.routers import DefaultRouter

from .views import InteractionViewSet

router = DefaultRouter()
router.register('', InteractionViewSet, basename='interactions')

urlpatterns = router.urls
