from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff) # Admin User
    

class FullDjangoModelPermissions(permissions.DjangoModelPermissions):
    """
    Use this when you want to assign a specific permissions to a particular endpoint
    without assigning a permission group to a user.
    """
    def __init__(self):
        # User can only has the `view` access on endpoint.
        self.perms_map["GET"] = ['%(app_label)s.view_%(model_name)s']
        
        
class ViewCustomerHistoryPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        # app.permission_name
        return request.user.has_perm('store.view_history')