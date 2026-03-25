from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.access.models import BusinessElement, AccessRoleRule, Role
from apps.access.serializers import (
    AccessRoleRuleSerializer,
    BusinessElementSerializer,
    RoleSerializer,
)
from apps.access.permissions import IsAdminRole


class RoleListView(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminRole, IsAuthenticated]


class AccessRoleRuleListCreatView(generics.CreateAPIView):
    queryset = AccessRoleRule.objects.select_related("role", "element").all()
    serializer_class = AccessRoleRuleSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


class BusinessElementListView(generics.ListAPIView):
    queryset = BusinessElement.objects.all()
    serializer_class = BusinessElementSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


class AccessRuleDeteilView(generics.RetrieveUpdateAPIView):
    queryset = AccessRoleRule.objects.select_related("role", "elemen").all()
    serializer_class = AccessRoleRuleSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
