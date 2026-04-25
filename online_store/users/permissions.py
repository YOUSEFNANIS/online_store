from rest_framework import permissions

class IsSeller(permissions.BasePermission):

    def has_permission(self, request, view):
        # 1. Check if the user is even logged in
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return hasattr(request.user, 'seller')
    
class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'customer')

class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view, obj):
        return request.user == obj.customer.user or request.user == obj.seller.user
    
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Admins can do anything
        if request.user and request.user.is_staff:
            return True

        # Only allow user to access their own object
        return obj.user == request.user