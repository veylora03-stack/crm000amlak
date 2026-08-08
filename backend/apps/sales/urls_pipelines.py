from rest_framework.routers import DefaultRouter

from .views import PipelineViewSet

router = DefaultRouter()
router.register('', PipelineViewSet, basename='pipelines')

urlpatterns = router.urls
