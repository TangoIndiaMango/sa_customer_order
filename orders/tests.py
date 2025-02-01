from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch
from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer
from decimal import Decimal

class CustomerViewSetTests(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Create test customer
        self.customer = Customer.objects.create(
            user=self.user,
            name="Timmy West",
            code="TIMYTESTCASE432",
            phone_number="+2348000321112"
        )
        
        self.customer_data = {
            "name": "Wellace Anderson",
            "code": "WELLACE342",
            "phone_number": "+2348000321112"
        }
        
    def test_create_customer(self):
        response = self.client.post('/api/customers/', self.customer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)
        
    def test_list_customers(self):
        response = self.client.get('/api/customers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_get_customer(self):
        response = self.client.get(f'/api/customers/{self.customer.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.customer.name)

class OrderViewSetTests(APITestCase):
    def setUp(self):
        # Create test user and customer
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.customer = Customer.objects.create(
            user=self.user,
            name="Timmy West",
            code="TIMYTESTCASE432",
            phone_number="+2348000321112"
        )
        
        self.order_data = {
            "customer": self.customer.id,
            "item": "Analysis In TeleMediine Book 1",
            "amount": "100.00"
        }
        
    @patch('orders.views.send_sms')
    def test_create_order(self, mock_send_sms):
        # Configure mock to return success
        mock_send_sms.return_value = "SMS sent successfully"
        
        response = self.client.post('/api/orders/', self.order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        mock_send_sms.assert_called_once()
        
    def test_list_orders(self):
        # Create a test order first
        Order.objects.create(
            customer=self.customer,
            item="Analysis In TeleMediine Book 1",
            amount=Decimal("100.00")
        )
        
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class SMSUtilsTests(TestCase):
    @patch('africastalking.SMS')
    def test_send_sms_success(self, mock_sms):
        from .utils import send_sms
        
        # Mock the SMS response
        mock_sms.send.return_value = {
            "SMSMessageData": {
                "Recipients": [{
                    "status": "Success",
                    "messageId": "test-id",
                    "cost": "0.00"
                }]
            }
        }
        
        result = send_sms("+2348000321112", "Test message")
        self.assertEqual(result, "SMS sent successfully")
        
    @patch('africastalking.SMS')
    def test_send_sms_failure(self, mock_sms):
        from .utils import send_sms
        
        mock_sms.send.return_value = {
            "SMSMessageData": {
                "Recipients": [{
                    "status": "Failed",
                    "messageId": None,
                    "cost": "0.00"
                }]
            }
        }
        
        result = send_sms("+2348000321112", "Test message")
        self.assertTrue(result.startswith("Failed to send SMS"))
        
        
