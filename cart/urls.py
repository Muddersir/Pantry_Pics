from django.urls import path
from .views import AddToCartView, CartView, RemoveCartItemView, DepositView

urlpatterns = [
    path("add/", AddToCartView.as_view(), name="cart-add"),
    path("", CartView.as_view(), name="cart-list"),
    path("item/<int:pk>/remove/", RemoveCartItemView.as_view(), name="cart-remove"),
    path("deposit/", DepositView.as_view(), name="deposit"),
]