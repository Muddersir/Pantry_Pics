from rest_framework import permissions

class IsSeller(permissions.BasePermission):
   
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, "is_seller", False))

class IsSellerOrReadOnly(permissions.BasePermission):
   
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and (request.user.is_staff or getattr(request.user, "is_seller", False)))

class IsOwnerOrAdmin(permissions.BasePermission):
   
    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        seller = getattr(obj, "seller", None)
        if request.user and request.user.is_staff:
            return True
        return bool(seller and seller == request.user)