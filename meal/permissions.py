from rest_framework import permissions

class CustomMealPermission(permissions.BasePermission):
    """
    Custom permission for MealViewSet.

    - Allow 'create', 'update', 'partial_update' actions only for admin users.
    - Allow 'list' action for authenticated users.
    - Deny all other actions.
    """

    def has_permission(self, request, view):
        if request.method in ['PUT', 'POST', 'PATCH']:
            return request.user and request.user.is_staff
        elif request.method == 'GET':
            return request.user and request.user.is_authenticated
        else:
            return False
