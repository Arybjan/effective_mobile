from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth / Users
    path("api/accounts/", include("apps.accounts.urls")),
]
