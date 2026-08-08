from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from apps.clients.models import Client

User = get_user_model()


class ClientCRUDTests(TestCase):
    def setUp(self):
        self.client_api = APIClient()
        self.user = User.objects.create_user(
            username='agent',
            password='agent123',
            email='agent@example.com',
            role='Agent'
        )
        
        login_response = self.client_api.post('/api/v1/auth/login/', {
            'identifier': 'agent',
            'password': 'agent123'
        })
        token = login_response.data['data']['access']
        self.client_api.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_create_client(self):
        response = self.client_api.post('/api/v1/clients/', {
            'full_name': 'علی رضایی',
            'phone': '09121111111',
            'email': 'ali@example.com',
            'source': 'اینستاگرام',
            'status': 'New',
            'customer_type': 'خریدار',
            'budget_min': 5000000000,
            'budget_max': 8000000000
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(Client.objects.count(), 1)

    def test_list_clients(self):
        Client.objects.create(
            full_name='علی رضایی',
            phone='09121111111',
            created_by=self.user
        )
        
        response = self.client_api.get('/api/v1/clients/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(len(response.data['data']), 1)

    def test_retrieve_client(self):
        client = Client.objects.create(
            full_name='علی رضایی',
            phone='09121111111',
            created_by=self.user
        )
        
        response = self.client_api.get(f'/api/v1/clients/{client.public_id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['full_name'], 'علی رضایی')

    def test_update_client(self):
        client = Client.objects.create(
            full_name='علی رضایی',
            phone='09121111111',
            created_by=self.user
        )
        
        response = self.client_api.patch(f'/api/v1/clients/{client.public_id}/', {
            'full_name': 'علی رضایی جدید'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        
        client.refresh_from_db()
        self.assertEqual(client.full_name, 'علی رضایی جدید')

    def test_delete_client(self):
        client = Client.objects.create(
            full_name='علی رضایی',
            phone='09121111111',
            created_by=self.user
        )
        
        response = self.client_api.delete(f'/api/v1/clients/{client.public_id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        
        client.refresh_from_db()
        self.assertTrue(client.is_deleted)

    def test_duplicate_phone_validation(self):
        Client.objects.create(
            full_name='علی رضایی',
            phone='09121111111',
            created_by=self.user
        )
        
        response = self.client_api.post('/api/v1/clients/', {
            'full_name': 'مریم احمدی',
            'phone': '09121111111',
            'email': 'maryam@example.com'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
