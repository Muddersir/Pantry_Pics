from django.urls import path
from .views import CheckoutView, OrderListView

urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("", OrderListView.as_view(), name="orders-list"),
]