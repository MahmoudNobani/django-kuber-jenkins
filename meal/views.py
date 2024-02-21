from rest_framework import generics
from collections import Counter
from .models import Meal, Order, Delivery
from employee.models import Employee
from .serializer import MealSerializer, OrderSerializer, DeliverySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets, mixins
from .permissions import CustomMealPermission
from .authentications import CustomMealAuthentication

class MealViewSet(viewsets.GenericViewSet,mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin):
    """
    General ViewSet Description:
    
    API view for creating, listing, retrieving, and updating Meals.

    create: Allow the addition of a new meal.
    list: List all the meals in the system 
    retrieve: Retrieve a specific meal.
    update: Update attributes of a meal.

    """

    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    #permission_classes = [CustomMealPermission]
    authentication_classes = [BasicAuthentication]
    

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAdminUser]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    # def initial(self, request, *args, **kwargs):
    #     # Set self.action based on the request method
    #     if request.method == 'POST':
    #         self.action = 'create'
    #     elif request.method == 'GET':
    #         if 'pk' in kwargs:
    #             self.action = 'retrieve'
    #         else:
    #             self.action = 'list'
    #     elif request.method == 'PATCH' or request.method == 'PUT':
    #         self.action = 'update'
    #     else:
    #         self.action = None
    #     super().initial(request, *args, **kwargs)
    

    
    #permission_classes = self.get_permissions()

    # def get_authenticators(self):
    #     print("33333333333333333333333333333333333333333")
    #     if self.action == 'create':
    #         authentication_classes = [BasicAuthentication]
    #     elif self.action in ['list', 'retrieve', 'update']:
    #         authentication_classes = [JWTAuthentication]
    #     else:
    #         authentication_classes = []
    #     return [authentication() for authentication in authentication_classes]

class OrderViewSet(viewsets.ModelViewSet):
    """
    General ViewSet Description:

    API view for creating, retrieving, updating, and deleting Orders.

    create: Creates a new Order.
    list: Lists all orders in the system.
    retrieve: Retrieves a specific order.
    partial_update: Partially updates order data (completed or delFlag).
    destroy: Deletes an order.

    """
    queryset = Order.objects.all()
    http_method_names = ["patch","get","delete","post"]
    serializer_class = OrderSerializer
    
    def create(self, request, *args, **kwargs):
        """
        create: Creates a new Order.

        Method:
            - POST

        Parameters:
            - data: Request data containing order details, including the list of meals.

        Response:
            - Status code: 201 if successful, 404 if invalid employee or meal IDs.
        """
        data=request.data
        meals_data = self.request.data.get('meal', [])
        sum = 0
        meal_obj = []

        try: 
            emp = Employee.objects.get(pk=data['empID'])
        except:
            return Response("invalid employee ID", status=status.HTTP_404_NOT_FOUND)
        
        for i in meals_data:
            try: 
                meal_temp = Meal.objects.get(pk=i)
                meal_obj.append(meal_temp)
                sum += meal_temp.price
            except:
                return Response("invalid Meal ID", status=status.HTTP_404_NOT_FOUND)
            
        meal_obj_counter = Counter(meal_obj)
               
        for i in meal_obj_counter.keys():
            try: 
                if i.capacity-meal_obj_counter[i] > 0:
                    i.capacity-=meal_obj_counter[i]
                if i.capacity-meal_obj_counter[i] <= 0:
                    raise ValueError("Meal is not available atm, please order something else")
                i.sales+=meal_obj_counter[i]
            except ValueError as e:
                return Response(str(e), status=status.HTTP_404_NOT_FOUND)  

        for i in meal_obj:
            i.save()             


        ord_obj = Order(empID= emp,
            price=sum,
            delFlag=data['delFlag'],
            completed= data['completed'])
        ord_obj.save()
        ord_obj.meal.set(meal_obj)
        
        ord_obj.save()
        
        for k, v in Counter(meal_obj).items():
            Order.meal.through.objects.filter(order=ord_obj, meal=k).update(quantity=v)

        data['price'] = sum
        return Response(data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk, *args, **kwargs):
        """
        destroy: Deletes an Order.

        Method:
            - DELETE

        Parameters:
            - pk: Primary key of the Order.
            - request: the request and its data

        Response:
            - Status code: 204 if successful, 404 if the Order is not found.
        """
        order_obj = Order.objects.get(pk=pk)
        meals_ids = order_obj.meal.through.objects.filter(order_id=pk)
            
        if order_obj.completed == False:
            for i in meals_ids:
                meal_obj = Meal.objects.get(pk=i.meal.pk)
                meal_obj.capacity+=i.quantity
                if meal_obj.sales-i.quantity > 0:
                    meal_obj.sales-=i.quantity
                else:
                    meal_obj.sales=0
                meal_obj.save()
        
        order_obj.delete()
        return Response({'message': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    def partial_update(self, request, pk, *args, **kwargs):
        """
        partial_update: Partially updates an Order's data (completed or delFlag).

        Method:
            - PATCH

        Parameters:
            - pk: Primary key of the Order.
            - request: Request data containing fields to be updated.

        Response:
            - Status code: 204 if successful, 404 if the Order is not found.
        """
        order_obj = Order.objects.get(pk=pk)
        if "completed" in request.data:
            if str(request.data['completed']) == 'False' or str(request.data['completed']) == 'false':
                order_obj.completed = 'False'
            else:
                order_obj.completed = 'True'

        if "delFlag" in request.data:
            if str(request.data['delFlag']) == 'False' or str(request.data['delFlag']) == 'false':
                order_obj.delFlag = 'False'
            else:
                order_obj.delFlag = 'True'
        order_obj.save()
        return Response({'message': 'Order edited successfully'}, status=status.HTTP_204_NO_CONTENT)

class DeliveryViewSet(viewsets.ModelViewSet):    
    """
    General ViewSet Description:

    API view for creating a new Delivery associated with an Order, return a list, retrivea an individual one, update, delete.
    
    get: get a delivery details
    patch: update a delivery
    delete: delete a delivery
    post: creates a delibery request with the needed data for an order
    """
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

    def create(self, request, *args, **kwargs):
        """
        create: Creates a new Delivery associated with an Order.

        Method:
            - POST

        Parameters:
            - data: Request data containing delivery details and associated order ID.
        Response:
            - Status code: 201 if successful, 404 if the order is not found or delivery is not allowed.
        """
        try:
            order_instance = Order.objects.get(pk=request.data["orderID"])
            # order_serializer = OrderSerializer(order_instance)
            # serialized_order_data = order_serializer.data
            if order_instance.delFlag is True:
                if order_instance.completed is False:
                    return super().create(request, *args, **kwargs)
                else:
                    return Response({'error': "the order cant have a delivery as the completed flag is True"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                return Response({'error': "the order cant have a delivery as the delivery flag is false"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        