from rest_framework import permissions


class IsAdminOrReadOnlyPermission(permissions.IsAdminUser):
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)
        
    
class IsAuthUserOrReadOnlyPermission(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.product_user == request.user or request.user.is_staff
        
class IsAdminOrReadOnlyGroupPermission(permissions.BasePermission):
    
    allowed_groups = ['Administrator', 'HR']
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # return bool(request.user and request.user.is_staff) or request.user.groups.filter(name='Administrator').exists()
        return bool(request.user and request.user.is_staff) or request.user.groups.filter(name__in=self.allowed_groups).exists()