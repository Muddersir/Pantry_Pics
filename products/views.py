from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from .models import Category, Product, Wishlist, Review
from .serializers import (
    CategorySerializer, ProductSerializer, CreateProductSerializer,
    WishlistSerializer, ReviewSerializer
)
from utils.permissions import IsSellerOrReadOnly, IsOwnerOrAdmin


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["price", "created_at"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateProductSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        user = self.request.user
        
        if not user.is_staff and not getattr(user, "is_seller", False):
            raise PermissionError("Only sellers or admin can create products")
        serializer.save(seller=user)


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsOwnerOrAdmin]  
    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return CreateProductSerializer
        return ProductSerializer

class AddToWishlistView(generics.CreateAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WishlistListView(generics.ListAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related("product", "product__category")

class RemoveFromWishlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, pk):
        wish = get_object_or_404(Wishlist, pk=pk, user=request.user)
        wish.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateReviewView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product = serializer.validated_data["product"]
        user = self.request.user
        # TODO: 
        serializer.save(user=user)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"
    queryset = Review.objects.all()

    def perform_update(self, serializer):
        review = self.get_object()
        if review.user != self.request.user:
            raise PermissionError("Cannot edit another user's review")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionError("Cannot delete another user's review")
        instance.delete()

class ProductDetailWithRatingView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product)
        avg = product.reviews.aggregate(avg_rating=Avg("rating"))["avg_rating"]
        data = serializer.data
        data["average_rating"] = avg or 0
        return Response(data)