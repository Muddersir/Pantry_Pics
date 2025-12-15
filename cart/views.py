from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import transaction
from .models import CartItem, Deposit
from .serializers import CartItemSerializer, DepositSerializer
from accounts.models import Profile

class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data.get("quantity", 1)
        user = self.request.user
        cart_item, created = CartItem.objects.get_or_create(user=user, product=product, defaults={"quantity": quantity})
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        self.created_obj = cart_item

class CartView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user).select_related("product", "product__category")

class RemoveCartItemView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CartItem.objects.all()

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionError("Cannot remove items from another user's cart")
        return obj

class DepositView(generics.CreateAPIView):
    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def perform_create(self, serializer):
        deposit = serializer.save(user=self.request.user)
        profile = getattr(self.request.user, "profile", None)
        if not profile:
            from accounts.models import Profile as ProfileModel
            profile = ProfileModel.objects.create(user=self.request.user)
        profile.wallet_balance += deposit.amount
        profile.save()