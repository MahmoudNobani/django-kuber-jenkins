from django.urls import path, include
# from .views import (
#     EmployeeListCreateView, EmployeeDetailView,
#     PhoneNumberListCreateView, PhoneNumberDetailView,
#     ListOrdersByEmp,
# )

from .views import EmployeeAdminViewSet, EmployeeViewSet, PhoneNumberViewSet, OrderAndEmpViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'admin', EmployeeAdminViewSet, basename='admin')
router.register(r'emp', EmployeeViewSet, basename='employee')
router.register(r'phone', PhoneNumberViewSet, basename='phone-number')
router.register(r'ObE', OrderAndEmpViewSet, basename='order')


urlpatterns = [
    path('', include(router.urls)),
    # path('ObE/<int:pk>/', OrderAndEmpViewSet.as_view({'get': 'list'}), name='orders-by-employee'),
    # path('', EmployeeListCreateView.as_view(), name='employee-list-create'),
    # path('<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),

    # path('phone/', PhoneNumberListCreateView.as_view(), name='phone-number-list'),
    # path('phone/<int:pk>/', PhoneNumberDetailView.as_view(), name='phone-number-detail'),
    
    # path('ObE/<int:employee_id>', ListOrdersByEmp.as_view(), name='Orders-By-Emp')
]