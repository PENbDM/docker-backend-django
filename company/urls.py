# users/urls.py

from django.urls import path
from .views import CompanyView, CompanyListView, CompanyMembersView, CompanyMemberView

urlpatterns = [
    path("make/", CompanyView.as_view()),
    path('get/', CompanyListView.as_view()),
    path("members/<int:company_id>/", CompanyMembersView.as_view()),
    path('member/<int:user_id>/',CompanyMemberView.as_view()),

]