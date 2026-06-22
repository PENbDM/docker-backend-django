from django.urls import path
from rest_framework.views import APIView

from .views import SavedQueryView,SavedQueryListView,QueryRunView,QueryRunListView,QueryResultView,QueryResultListView

urlpatterns = [
    path('post-saved-query/',SavedQueryView.as_view()),
    path('get-saved-query/<int:company_id>/',SavedQueryListView.as_view()),
    path('post-run-query/',QueryRunView.as_view()),
    path('get-run-query/<int:company_id>/',QueryRunListView.as_view()),
    path('post-result-query/',QueryResultView.as_view()),
    path('get-result-query/<int:query_run_id>/',QueryResultListView.as_view()),
]