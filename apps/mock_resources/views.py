from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.access.services import has_access, get_role_rule


MOCK_PRODUCTS = [
    {"id": 1, "name": "MacBook Pro", "owner_id": 1},
    {"id": 2, "name": "ThinkPad X1", "owner_id": 2},
    {"id": 3, "name": "iPhone 15", "owner_id": 1},
]

MOCK_ORDERS = [
    {"id": 1, "title": "Order #1001", "owner_id": 1},
    {"id": 2, "title": "Order #1002", "owner_id": 2},
    {"id": 3, "title": "Order #1003", "owner_id": 1},
]

MOCK_USERS = [
    {"id": 1, "email": "admin@example.com", "owner_id": 1},
    {"id": 2, "email": "user1@example.com", "owner_id": 2},
    {"id": 3, "email": "user2@example.com", "owner_id": 3},
]


class ProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        role = get_role_rule(user, "products")

        if not role:
            return Response(
                {"detail": "Нет доступа к ресурсу products"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if role.read_all_permission:
            return Response(MOCK_PRODUCTS, status=status.HTTP_200_OK)

        if role.read_permission:
            own_products = [
                item for item in MOCK_PRODUCTS if item["owner_id"] == user.id
            ]
            return Response(own_products, status=status.HTTP_200_OK)

        return Response(
            {"detail": "У вас нет доступа к просмотру products"},
            status=status.HTTP_403_FORBIDDEN,
        )

    def post(self, request):
        user = request.user

        if not has_access(user, "products", "create"):
            return Response(
                {"detail": "У вас нет доступа к созданию products"},
                status=status.HTTP_403_FORBIDDEN,
            )

        new_item = {
            "id": len(MOCK_PRODUCTS) + 1,
            "name": request.data.get("name", "New product"),
            "owner_id": user.id,
        }
        return Response(new_item, status=status.HTTP_201_CREATED)


class OrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        role = get_role_rule(user, "orders")

        if not role:
            return Response(
                {"detail": "Нет доступа к ресурсу orders"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if role.read_all_permission:
            return Response(MOCK_ORDERS, status=status.HTTP_200_OK)

        if role.read_permission:
            own_orders = [item for item in MOCK_ORDERS if item["owner_id"] == user.id]
            return Response(own_orders, status=status.HTTP_200_OK)

        return Response(
            {"detail": "У вас нет доступа к просмотру orders"},
            status=status.HTTP_403_FORBIDDEN,
        )

    def post(self, request):
        user = request.user

        if not has_access(user, "orders", "create"):
            return Response(
                {"detail": "У вас нет доступа к созданию orders"},
                status=status.HTTP_403_FORBIDDEN,
            )

        new_order = {
            "id": len(MOCK_PRODUCTS) + 1,
            "title": request.data.get("title", "New order"),
            "owner_id": user.id,
        }
        return Response(new_order, status=status.HTTP_201_CREATED)

    def putch(self, request):
        user = request.user
        order_id = request.data.get("id")

        order = next((item for item in MOCK_ORDERS if item["id"] == order_id), None)
        if not order:
            return Response(
                {"detail": "Order не найден"}, status=status.HTTP_404_NOT_FOUND
            )

        is_owner = order["owner"] == user.id

        if not has_access(user, "orders", "update", is_owner=is_owner):
            return Response(
                {"detail": "У вас нет доступа к изменению orders"},
                status=status.HTTP_403_FORBIDDEN,
            )

        order["title"] = request.data.get("title", order["title"])
        return Response(order, status=status.HTTP_200_OK)

    def delete(self, request):
        user = request.user
        order_id = request.data.get("id")

        order = next((item for item in MOCK_ORDERS if item["id"] == order_id), None)
        if not order:
            return Response(
                {"detail": "Order не найден."},
                status=status.HTTP_404_NOT_FOUND,
            )

        is_owner = order["owner_id"] == user.id

        if not has_access(user, "orders", "delete", is_owner=is_owner):
            return Response(
                {"detail": "У вас нет доступа к удалению orders"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(
            {"message": f"Order {order_id} удален"},
            status=status.HTTP_200_OK,
        )


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        role = get_role_rule(user, "users")

        if not role:
            return Response(
                {"detail": "Нет доступа к ресурсу users"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if role.read_all_permission:
            return Response(MOCK_USERS, status=status.HTTP_200_OK)

        if role.read_permission:
            own_user_data = [item for item in MOCK_USERS if item["id"] == user.id]
            return Response(own_user_data, status=status.HTTP_200_OK)

        return Response(
            {"detail": "У вас нет доступа к просмотру users."},
            status=status.HTTP_403_FORBIDDEN,
        )
