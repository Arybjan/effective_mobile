from django.urls import path
from .views import (
    RoleListView,
    AccessRoleRuleListCreatView,
    BusinessElementListView,
    AccessRuleDetailView,
)

urlpatterns = [
    path("roles/", RoleListView.as_view(), name="roles"),
    path("elements", BusinessElementListView.as_view(), name="elements"),
    path("rules", AccessRoleRuleListCreatView.as_view(), name="rules"),
    path("rules/<int:pk>/", AccessRuleDetailView.as_view(), name="rule-detail"),
]
