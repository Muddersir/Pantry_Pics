from rest_framework import serializers
from .models import CartItem, Deposit
from products.serializers import ProductSerializer
from products.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(is_active=True),
        source="product",
        write_only=True
    )

    class Meta:
        model = CartItem
        fields = ("id", "product", "product_id", "quantity", "added_at")

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ("id", "amount", "created_at")
        read_only_fields = ("created_at",)