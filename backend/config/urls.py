from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API v1
    path('api/v1/auth/', include('apps.accounts.urls_auth')),
    path('api/v1/users/', include('apps.accounts.urls_users')),
    path('api/v1/clients/', include('apps.clients.urls')),
    path('api/v1/properties/', include('apps.properties.urls')),
    path('api/v1/pipelines/', include('apps.sales.urls_pipelines')),
    path('api/v1/stages/', include('apps.sales.urls_stages')),
    path('api/v1/deals/', include('apps.sales.urls_deals')),
    path('api/v1/interactions/', include('apps.activities.urls')),
    path('api/v1/tasks/', include('apps.tasks.urls')),
    path('api/v1/dashboard/', include('apps.dashboard.urls')),
    path('api/v1/reports/', include('apps.reports.urls')),
    path('api/v1/notifications/', include('apps.notifications.urls')),
    path('api/v1/settings/', include('apps.core.urls_settings')),
    path('api/v1/search/', include('apps.core.urls_search')),
    path('api/v1/audit-logs/', include('apps.audit.urls')),
    path('api/v1/ai/', include('apps.ai.urls')),
    
    # API Docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
