from rest_framework import generics, permissions
from products.models import Product
from orders.models import Order, OrderItem
from .serializers import SellerProductSerializer, SellerOrdersSerializer
from utils.permissions import IsSeller

class SellerProductListView(generics.ListAPIView):
    serializer_class = SellerProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsSeller]

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)

class SellerSalesView(generics.ListAPIView):
    serializer_class = SellerOrdersSerializer
    permission_classes = [permissions.IsAuthenticated, IsSeller]

    def get_queryset(self):
        
        order_ids = OrderItem.objects.filter(seller=self.request.user).values_list("order_id", flat=True).distinct()
        return Order.objects.filter(id__in=order_ids).prefetch_related("items__product")