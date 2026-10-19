from rest_framework import permissions

from core.order_flow import owner_of

class IsSeller(permissions.BasePermission):

    def has_permission(self, request, view):
        # 1. Check if the user is even logged in
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return hasattr(request.user, 'seller')
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:    
            return True
        return request.user == obj.seller.user
    
class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        # owner_of reads customer_pk from the auth query, so no profile query.
        return request.user.is_authenticated and owner_of(request.user)[0] == 'customer'

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Compare ids so the user rows are not loaded. customer is null after the customer is deleted.
        customer_user_id = obj.customer.user_id if obj.customer_id else None
        return request.user.id in (customer_user_id, obj.seller.user_id)

class IsCartItemOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # cart is select_related in the view, so this compares ids with no query.
        return obj.cart.customer_id == owner_of(request.user)[1]
    
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # Signup (create) is open; list is staff-only; everything else needs a login.
        if view.action == 'create':
            return True
        if view.action == 'list':
            return bool(request.user and request.user.is_staff)
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True

        return obj.user == request.user


class ReviewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return hasattr(request.user, 'customer')

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.customer.user_id == request.user.id


class IsProductOwnerOrReadOnly(permissions.BasePermission):
    """Product images (nested under /products/<products_pk>/): only the product's seller may change them."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        seller = getattr(request.user, 'seller', None)
        return bool(seller) and seller.product_set.filter(pk=view.kwargs['products_pk']).exists()


class IsSellerAccount(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'seller')
