from apps.access.models import AccessRoleRule


def get_role_rule(user, element_code: str):
    if not user or not getattr(user, "role", None):
        return None
    return (
        AccessRoleRule.objects.select_related("role", "element")
        .filter(role=user.role, element__code=element_code)
        .first()
    )


def can_read(rule, is_owner: bool = False) -> bool:
    if not rule:
        return False
    return rule.read_all_permission or (rule.read_permmission and is_owner)


def can_create(rule) -> bool:
    if not rule:
        return False
    return rule.create_permission


def can_update(rule, is_owner: bool = False) -> bool:
    if not rule:
        return False
    return rule.update_all_permission or (rule.update_permission and is_owner)


def can_delete(rule, is_owner: bool = False) -> bool:
    if not rule:
        return False
    return rule.delete_all_permission or (rule.delete_permission and is_owner)

def has_access(user, element_code: str, action: str, is_owner: bool = False) -> bool:
    rule = get_role_rule(user, element_code)

    if action == "read":
        return can_read(rule, is_owner=is_owner)
    
    if action == "update":
        return can_update(rule, is_owner=is_owner)
    
    if action == "create":
        return can_create(rule)
    
    if action == "delete":
        return can_delete(rule, is_owner=is_owner)

    return False
