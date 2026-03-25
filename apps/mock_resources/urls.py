from django.urls import path
from .views import UserView, ProductView, OrdersView

urlpattrns = [
    path("products/", ProductView.as_view(), name="products"),
    path("orders/", OrdersView.as_view(), name="orders"),
    path("users/", UserView.as_view(), name="users"),
]
