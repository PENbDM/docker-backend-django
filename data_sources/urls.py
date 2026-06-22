from django.urls import path
from rest_framework.views import APIView

from .views import DatabaseConnectionView, DataTableView, SyncTablesView, DataColumnView, TablePermissionView, \
    SyncColumnsView

urlpatterns = [
    path('connect/',DatabaseConnectionView.as_view()),
    path('<int:connection_id>/get-table/',DataTableView.as_view()),
    path('<int:connection_id>/sync-table/',SyncTablesView.as_view()),
    path('tables/<int:table_id>/columns/',DataColumnView.as_view()),
    path('<int:connection_id>/sync-column/',SyncColumnsView.as_view()),
    path('post-table-permission/',TablePermissionView.as_view()),
]