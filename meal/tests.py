from django.test import TestCase
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .serializer import MealSerializer, OrderSerializer, DeliverySerializer
from .models import Meal, Order, Delivery
from employee.models import Employee, PhoneNumber
from employee.serializer1 import EmployeeSerializer  
from .serializer import MealSerializer

#DB tests
@pytest.mark.django_db
def test_meal_str(create_test_data):
    """
    Test if the created meal model was created.

    Parameters:
        create_test_data (fixture): A fixture providing test data.

    Returns:
        None
    """
    meal1 = create_test_data['meal1']
    assert str(meal1) == 'Burger'

@pytest.mark.django_db
def test_order_str(create_test_data):
    """
    Test if Order was created.

    Parameters:
        create_test_data (fixture): A fixture providing test data.

    Returns:
        None
    """
    order = create_test_data['order']
    emp = create_test_data['employee']
    assert order.empID == emp
    assert order.price == 35.97
 
@pytest.mark.django_db
def test_delivery_str(create_test_data):
    """
    Test if Delivery id created.

    Parameters:
        create_test_data (fixture): A fixture providing test data.

    Returns:
        None
    """
    delivery = create_test_data['delivery']
    order = create_test_data['order']
    assert delivery.orderID == order
    assert delivery.name == 'John Doe'


#view test
@pytest.mark.django_db
def test_meal_list_create_view(admin_user, create_test_data):
    """
    Test the Meal list and create views.

    Parameters:
        admin_user: A Django user with admin privileges.
        create_test_data (fixture): A fixture providing test data.

    Returns:
        None
    """
    client = APIClient()
    url = reverse('meal-list')
    data = {'name': 'New Meal', 'price': 9.99, 'capacity': 30, 'sales': 5}

    client.force_authenticate(admin_user)
    # Create a new meal
    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED

    url = reverse('meal-list')
    # Check if the meal is listed
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 4  # Assuming there are already 3 meals from the fixture

@pytest.mark.django_db
def test_meal_list_create_perm_view(normal_user, create_test_data):
    """
    Test the Meal list and create views.

    Parameters:
        admin_user: A Django user with admin privileges.
        create_test_data (fixture): A fixture providing test data.

    Returns:
        None
    """
    client = APIClient()
    url = reverse('meal-list')
    data = {'name': 'New Meal', 'price': 9.99, 'capacity': 30, 'sales': 5}

    client.force_authenticate(normal_user)
    # Create a new meal
    response = client.post(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    url = reverse('meal-list')
    # Check if the meal is listed
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_update_meal(admin_user, create_test_data):
    """
    Test updating a Meal.

    Parameters:
        admin_user: A Django user with admin privileges.
        create_test_data (fixture): A fixture providing test data.

    Returns:
        None
    """
    client = APIClient()
    client.force_authenticate(admin_user)
    meal_id = create_test_data['meal1'].id
    url = reverse('meal-detail', kwargs={'pk': meal_id})

    # New data to update the meal
    #updated_data = {"name": "qer","price": 9.0,"capacity": 13,"sales": 10}
    updated_data = {
        "name": "pizza",
        "price": 12.0,
        "capacity": 20,
        "sales": 12
    }

    # Update the meal
    response = client.patch(url, data=updated_data)
    assert response.status_code == status.HTTP_200_OK

    url = reverse('meal-detail', kwargs={'pk': meal_id})
    # Ensure the meal is updated
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == updated_data['name']
    assert response.data['price'] == updated_data['price']
    assert response.data['capacity'] == updated_data['capacity']
    assert response.data['sales'] == updated_data['sales']

@pytest.mark.django_db
def test_update_perm_meal(normal_user, create_test_data):
    """
    Test updating a Meal.

    Parameters:
        admin_user: A Django user with admin privileges.
        create_test_data (fixture): A fixture providing test data.

    Returns:
        None
    """
    client = APIClient()
    #client.force_authenticate(normal_user)
    meal_id = create_test_data['meal1'].id
    url = reverse('meal-detail', kwargs={'pk': meal_id})

    # New data to update the meal
    #updated_data = {"name": "qer","price": 9.0,"capacity": 13,"sales": 10}
    updated_data = {
        "name": "pizza",
        "price": 12.0,
        "capacity": 20,
        "sales": 12
    }

    # Update the meal
    response = client.patch(url, data=updated_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_order_delete_view(client, create_test_data):
    """
    Test deleting an Order.

    Parameters:
        client: Django test client.
        create_test_data (fixture): A fixture providing test data.

    Returns:
        None
    """
    order_id = create_test_data['order'].id
    url = reverse('order-detail', kwargs={'pk': order_id})

    response = client.get(url)
    # Delete an order
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # # Ensure the order is deleted
    # response = client.get(url)
    # assert response.status_code == status.HTTP_404_NOT_FOUND
    
@pytest.mark.django_db
def test_add_order(client, create_test_data):
    """
    Test adding an Order.

    Parameters:
        client: Django test client.
        create_test_data (fixture): A fixture providing test data.

    Returns:
        None
    """
    employee = create_test_data['employee']
    url = reverse('order-list')

    employee_data = EmployeeSerializer(employee).data
    meal1 = MealSerializer(create_test_data['meal1']).data
    meal2 = MealSerializer(create_test_data['meal2']).data
    new_order_data = {
        'empID': employee_data['id'],
        'price': 20.0,
        'delFlag': False,
        "completed": False,
        'meal': [meal1["id"], meal2["id"], meal2["id"]]
    }

    response = client.post(url, data=new_order_data, content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_list_orders(client, create_test_data):
    """
    Test listing Orders.

    Parameters:
        client: Django test client.
        create_test_data (fixture): A fixture providing test data.

    Returns:
        None
    """
    url = reverse('order-list')

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1  # One order should be in the list

@pytest.mark.django_db
def test_patial_update_order(client, create_test_data):
    """
    Test partially updating an Order.

    Parameters:
        client: Django test client.
        create_test_data (fixture): A fixture providing test data.

    Returns:
        None
    """
    order = create_test_data['order']
    url = reverse('order-detail', kwargs={'pk': order.pk})

    updated_order_data = {
        'completed': True,
    }

    response = client.patch(url, data=updated_order_data, content_type='application/json')
    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.django_db
class TestDeliveryViewSet:
    """
    test for delivey viewset
    """
    def test_create_delivery_successful(self,del_order):
        """
        Test creating a delivery successfully.

        Args: 
            del_order: order object to be tested
        """
        data = {
            "orderID": del_order.pk,
            "name": "Mahmoud",
            "address": "nablus",
        }

        client = APIClient()

        url = reverse('delivery-list')

        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert Delivery.objects.count() == 1

    def test_create_delivery_order_not_found(self,del_order):
        """
        Test creating a delivery with a non-existing order ID.

        Args: 
            del_order: order object to be tested
        """
        data = {
            "orderID": 999, 
            "name": "Mahmoud",
            "address": "nablus",
        }

        client = APIClient()

        url = reverse('delivery-list')

        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_delivery_order_completed(self,del_order):
        """
        Test creating a delivery when the order is marked as completed.

        Args: 
            del_order: order object to be tested
        """
        del_order.completed = True
        del_order.save()

        data = {
            "orderID": del_order.pk,
            "name": "Mahmoud",
            "address": "nablus",
        }

        client = APIClient()

        url = reverse('delivery-list')
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_delivery_delivery_flag_false(self, del_order):
        """
        Test creating a delivery when the order's delivery flag is set to False.

        Args: 
            del_order: order object to be tested
        """
        del_order.delFlag = False
        del_order.save()

        data = {
            "orderID": del_order.pk,
            "name": "Mahmoud",
            "address": "nablus",
        }

        client = APIClient()

        url = reverse('delivery-list')
        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
