from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            role='Agent'
        )

    def test_login_with_valid_credentials(self):
        response = self.client.post('/api/v1/auth/login/', {
            'identifier': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('access', response.data['data'])
        self.assertIn('refresh', response.data['data'])

    def test_login_with_invalid_credentials(self):
        response = self.client.post('/api/v1/auth/login/', {
            'identifier': 'testuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])

    def test_get_me_with_valid_token(self):
        login_response = self.client.post('/api/v1/auth/login/', {
            'identifier': 'testuser',
            'password': 'testpass123'
        })
        token = login_response.data['data']['access']
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/v1/auth/me/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['username'], 'testuser')

    def test_get_me_without_token(self):
        response = self.client.get('/api/v1/auth/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserManagementTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='admin',
            password='admin123',
            email='admin@example.com',
            role='Admin'
        )
        self.agent = User.objects.create_user(
            username='agent',
            password='agent123',
            email='agent@example.com',
            role='Agent'
        )

    def test_admin_can_list_users(self):
        login_response = self.client.post('/api/v1/auth/login/', {
            'identifier': 'admin',
            'password': 'admin123'
        })
        token = login_response.data['data']['access']
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/v1/users/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

    def test_agent_cannot_list_users(self):
        login_response = self.client.post('/api/v1/auth/login/', {
            'identifier': 'agent',
            'password': 'agent123'
        })
        token = login_response.data['data']['access']
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/v1/users/')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
