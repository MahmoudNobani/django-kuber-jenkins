from rest_framework.authentication import BaseAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomMealAuthentication(BaseAuthentication):
    """
    Custom authentication for MealViewSet.

    - Use BasicAuthentication for 'create', 'update', 'partial_update' actions.
    - Use JWTAuthentication for 'list' action.
    - No authentication for other actions.
    """

    def authenticate(self, request):
        if request.method in ['POST', 'PUT', 'PATCH']:
            return BasicAuthentication
        elif request.method == 'GET':
            return JWTAuthentication
        return None
