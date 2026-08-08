from django.urls import path

from .views import DashboardChartsView, DashboardKpisView, DashboardRecentActivitiesView

urlpatterns = [
    path('kpis/', DashboardKpisView.as_view(), name='dashboard-kpis'),
    path('charts/', DashboardChartsView.as_view(), name='dashboard-charts'),
    path('recent-activities/', DashboardRecentActivitiesView.as_view(), name='dashboard-recent-activities'),
]
