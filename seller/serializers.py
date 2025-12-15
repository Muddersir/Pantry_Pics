from rest_framework import serializers
from products.serializers import ProductSerializer
from orders.serializers import OrderSerializer
from products.models import Product
from orders.models import Order

class SellerProductSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        model = Product
        fields = ProductSerializer.Meta.fields

class SellerOrdersSerializer(OrderSerializer):
    class Meta(OrderSerializer.Meta):
        model = Order
        fields = OrderSerializer.Meta.fields