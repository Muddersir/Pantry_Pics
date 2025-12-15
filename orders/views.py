from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import transaction
from django.shortcuts import get_object_or_404
from cart.models import CartItem
from accounts.models import Profile
from .models import Order, OrderItem
from .serializers import OrderSerializer
from utils.email_service import send_order_confirmation

class CheckoutView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = request.user
        cart_items = CartItem.objects.filter(user=user).select_related("product")
        if not cart_items.exists():
            return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        total = 0
        for item in cart_items:
            if not item.product.is_active:
                return Response({"detail": f"Product {item.product.title} is not available"}, status=status.HTTP_400_BAD_REQUEST)
            if item.quantity > item.product.quantity:
                return Response({"detail": f"Insufficient stock for {item.product.title}"}, status=status.HTTP_400_BAD_REQUEST)
            total += item.product.price * item.quantity

        profile = getattr(user, "profile", None)
        if not profile:
            return Response({"detail": "User profile missing"}, status=status.HTTP_400_BAD_REQUEST)
        if profile.wallet_balance < total:
            return Response({"detail": "Insufficient balance. Please deposit funds."}, status=status.HTTP_400_BAD_REQUEST)

        
        profile.wallet_balance -= total
        profile.save()

       
        order = Order.objects.create(user=user, total_amount=total, status="PROCESSING")
      
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                seller=item.product.seller,
                price=item.product.price,
                quantity=item.quantity
            )
           
            item.product.quantity = max(0, item.product.quantity - item.quantity)
            item.product.save()
       
        cart_items.delete()

        
        try:
            send_order_confirmation(order)
        except Exception:
          
            pass

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items__product")