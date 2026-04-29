from rest_framework import permissions

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
        return hasattr(request.user, 'customer')

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.customer.user or request.user == obj.seller.user

class IsCartItemOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.cart.customer.user == request.user
    
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True

        return obj.user == request.user