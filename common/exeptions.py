from rest_framework.exceptions import AuthenticationFailed, PermissionDenied


class CustomAuthenticationFailed(AuthenticationFailed):
    default_detail = "Не удалось аутентифицировать пользователя."


class CustomPerissionDenied(PermissionDenied):
    default_detail = "У вас нет доступа к этому ресурсу."
