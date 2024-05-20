from rest_framework import permissions


class OnlyAdmin(permissions.BasePermission):
        
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user.is_authenticated
        # Check if the user is authenticated and has the role 'admin'
        return request.user.is_authenticated and request.user.role == 'admin'
    
