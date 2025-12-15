from rest_framework import serializers
from .models import Category, Product, Wishlist, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True, required=False
    )
    seller = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = ("id", "title", "description", "price", "quantity", "is_active", "category", "category_id", "seller", "created_at")

class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("title", "description", "price", "quantity", "is_active", "category")

class WishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.filter(is_active=True), source="product", write_only=True)

    class Meta:
        model = Wishlist
        fields = ("id", "product", "product_id", "created_at")

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.filter(is_active=True), source="product", write_only=True)

    class Meta:
        model = Review
        fields = ("id", "user", "product", "product_id", "rating", "comment", "created_at", "updated_at")
        read_only_fields = ("product", "user", "created_at", "updated_at")