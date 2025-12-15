from django.urls import path
from .views import SellerProductListView, SellerSalesView

urlpatterns = [
    path("products/", SellerProductListView.as_view(), name="seller-products"),
    path("sales/", SellerSalesView.as_view(), name="seller-sales"),
]