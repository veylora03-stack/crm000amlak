from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient
from rest_framework import status

from apps.tasks.models import Task

User = get_user_model()


class TaskCRUDTests(TestCase):
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

    def test_create_task(self):
        response = self.client_api.post('/api/v1/tasks/', {
            'title': 'تماس با علی رضایی',
            'description': 'پیگیری بازدید دوم',
            'priority': 'High',
            'status': 'Todo',
            'due_date': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
            'due_time': '14:00'
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(Task.objects.count(), 1)

    def test_list_tasks(self):
        Task.objects.create(
            title='تماس با علی رضایی',
            priority='High',
            status='Todo',
            due_date=timezone.now().date(),
            created_by=self.user
        )
        
        response = self.client_api.get('/api/v1/tasks/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(len(response.data['data']), 1)

    def test_complete_task(self):
        task = Task.objects.create(
            title='تماس با علی رضایی',
            priority='High',
            status='Todo',
            due_date=timezone.now().date(),
            created_by=self.user
        )
        
        response = self.client_api.post(f'/api/v1/tasks/{task.public_id}/complete/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        
        task.refresh_from_db()
        self.assertEqual(task.status, 'Done')
        self.assertIsNotNone(task.completed_at)

    def test_update_task(self):
        task = Task.objects.create(
            title='تماس با علی رضایی',
            priority='High',
            status='Todo',
            due_date=timezone.now().date(),
            created_by=self.user
        )
        
        response = self.client_api.patch(f'/api/v1/tasks/{task.public_id}/', {
            'title': 'تماس با علی رضایی - ویرایش شده',
            'priority': 'Medium'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        
        task.refresh_from_db()
        self.assertEqual(task.title, 'تماس با علی رضایی - ویرایش شده')
        self.assertEqual(task.priority, 'Medium')

    def test_delete_task(self):
        task = Task.objects.create(
            title='تماس با علی رضایی',
            priority='High',
            status='Todo',
            due_date=timezone.now().date(),
            created_by=self.user
        )
        
        response = self.client_api.delete(f'/api/v1/tasks/{task.public_id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        
        task.refresh_from_db()
        self.assertTrue(task.is_deleted)
