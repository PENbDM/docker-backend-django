# main urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("user.urls")),
    path('api/company/',include('company.urls')),
    path('api/db-connection/',include('data_sources.urls')),
    path('api/queries/',include('queries.urls')),
    # path("api/token/", TokenObtainPairView.as_view()),
    # path("api/token/refresh/", TokenRefreshView.as_view()),

]