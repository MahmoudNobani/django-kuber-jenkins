import json
from rest_framework import generics
from rest_framework.views import APIView
from .models import PhoneNumber, Employee
from rest_framework.response import Response
from .serializer1 import EmployeeSerializer,PhoneNumberSerializer,EmpSerWithPhone
from meal.models import Order
from meal.serializer import OrderSerializer
from rest_framework import status 
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework import viewsets
from .permissions import IsAuthorOrReadOnly

#FINAL VERSION OF VIEWS USING GENERICS

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    general viewset description
    View for listing, creating, retrieving, updating, and deleting Employee instances.
    Supports GET, POST, PATCH, and DELETE methods.

    List: list all employees
    create: create all employees, this API also accepts phone numbers with it
    retrieve: retrieve data for an employee with the associated phone number
    partial update: partially updates employee data
    delete: delete employee data

    Only accessible to admin users with basic authentication.
    """
    permission_classes = [IsAuthorOrReadOnly]
    authentication_classes = [BasicAuthentication]
    queryset = Employee.objects.all()
    serializer_class = EmpSerWithPhone
    http_method_names = ["patch","get"]

    def get_queryset(self):
        employee_id = self.kwargs['pk']
        return Employee.objects.filter(id=employee_id)


class EmployeeAdminViewSet(viewsets.ModelViewSet):
    """
    general viewset description
    View for listing, creating, retrieving, updating, and deleting Employee instances.
    Supports GET, POST, PATCH, and DELETE methods.

    List: list all employees
    create: create all employees, this API also accepts phone numbers with it
    retrieve: retrieve data for an employee with the associated phone number
    partial update: partially updates employee data
    delete: delete employee data

    Only accessible to admin users with basic authentication.
    """
    permission_classes = [IsAdminUser]
    authentication_classes = [BasicAuthentication]
    queryset = Employee.objects.all()
    serializer_class = EmpSerWithPhone
    http_method_names = ["patch","get","delete","post"]


class PhoneNumberViewSet(viewsets.ModelViewSet):
    """
    general viewset description
    View for listing, creating, retrieving, updating, and deleting PhoneNumber instances.
    Supports GET, POST, PATCH, and DELETE methods.

    List: list all phone numbers
    create: create phone for an existing employee
    retrieve: retrieve a specific phone number
    update: update a specific phone number
    delete: delete a specific phone number

    No specific permissions are set.
    """
    # No specific permissions are set.
    queryset = PhoneNumber.objects.all()
    serializer_class = PhoneNumberSerializer


class OrderAndEmpViewSet(viewsets.ReadOnlyModelViewSet):
    """
    general viewset description
    View for listing orders associated with a specific employee.

    retrive: get the order associated with a specific employee
    list: DOESNT WORK, DONT USE IT
    """
    serializer_class = OrderSerializer

    def get_queryset(self):
        employee_id = self.kwargs['pk']
        return Order.objects.filter(empID=employee_id)
    
    def list(self, request, *args, **kwargs):
        return Response({'error': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': 'resource not found'}, status=status.HTTP_404_NOT_FOUND)
