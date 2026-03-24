from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from apps.accounts.models import User, UserSession
from common.utils import decode_access_token


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "Bearer":
            raise AuthenticationFailed("Некорректный формат Authorization header")

        token = parts[1]

        try:
            payload = decode_access_token(token=token)
        except Exception:
            raise AuthenticationFailed("Токен недействителен или просрочен")

        user_id = payload.get("user_id")
        if not user_id:
            raise AuthenticationFailed("В токене отсутствует user_id")

        try:
            user = User.objects.get(id=user_id, is_active=True)
        except User.DoesNotExist:
            raise AuthenticationFailed("Пользователь не найден или деактивирован")

        session_exits = UserSession.objects.filter(
            user=user, token=token, is_active=True
        ).exists()

        if not session_exits:
            raise AuthenticationFailed("Сессия не активна, выполните вход занаво")
        
        return (user, token)