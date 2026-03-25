from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # Auth / Users
    path("api/accounts/", include("apps.accounts.urls")),
    # Role / Access rules
    path("api/access/", include("apps.access.urls")),
    # Mock business endpoints
    path("api/mock/", include("apps.mock_pesources.urls")),
]
