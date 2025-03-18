from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'owner'

class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'user'


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow restaurant owner users to perform all actions,
    but normal users can only perform read actions (GET, HEAD, OPTIONS).
    """
    def has_permission(self, request, view):
        # Allow any authenticated user to perform SAFE_METHODS
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Allow only owner users to perform other methods
        return request.user.is_authenticated and request.user.role == 'owner'
