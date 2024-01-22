from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MealViewSet, OrderViewSet, DeliveryViewSet

router = DefaultRouter()
router.register(r'MealApp', MealViewSet, basename='meal')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'deli',DeliveryViewSet,basename="delivery")

urlpatterns = [
    path('', include(router.urls)),
]