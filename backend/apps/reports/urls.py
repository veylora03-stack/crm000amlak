from django.urls import path

from .views import (
    ReportAgentsView,
    ReportDealsView,
    ReportExportView,
    ReportFunnelView,
    ReportLeadsView,
    ReportPropertiesView
)

urlpatterns = [
    path('leads/', ReportLeadsView.as_view(), name='report-leads'),
    path('deals/', ReportDealsView.as_view(), name='report-deals'),
    path('agents/', ReportAgentsView.as_view(), name='report-agents'),
    path('funnel/', ReportFunnelView.as_view(), name='report-funnel'),
    path('properties/', ReportPropertiesView.as_view(), name='report-properties'),
    path('export/', ReportExportView.as_view(), name='report-export'),
]
