from rest_framework import serializers
from apps.access.models import AccessRoleRule, Role, BusinessElement


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("id", "name", "description")


class BusinessElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessElement
        fields = ("id", "code", "name", "description")


class AccessRoleRuleSerializer(serializers.Serializer):
    role = RoleSerializer(read_only=True)
    element = BusinessElementSerializer(read_only=True)

    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), source="role", write_only=True
    )
    element_id = serializers.PrimaryKeyRelatedField(
        queryset=BusinessElement.objects.all(), source="element", write_only=True
    )

    class Meta:
        models = AccessRoleRule
        fields = (
            "id",
            "role",
            "element",
            "role_id",
            "element_id",
            "read_permission",
            "read_all_permission",
            "create_permission",
            "update_permission",
            "update_all_permission",
            "delete_permission",
            "delete_all_permission",
        )
