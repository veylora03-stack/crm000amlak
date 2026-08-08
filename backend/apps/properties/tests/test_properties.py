from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from apps.properties.models import Property

User = get_user_model()


class PropertyCRUDTests(TestCase):
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

    def test_create_property(self):
        response = self.client_api.post('/api/v1/properties/', {
            'code': 'AP-1001',
            'title': 'آپارتمان 85 متری سعادت‌آباد',
            'property_type': 'آپارتمان',
            'listing_type': 'فروش',
            'status': 'Draft',
            'publish_status': 'Draft',
            'price': 7500000000,
            'building_area': 85,
            'bedrooms': 2,
            'city': 'تهران',
            'district': 'سعادت‌آباد'
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(Property.objects.count(), 1)

    def test_list_properties(self):
        Property.objects.create(
            code='AP-1001',
            title='آپارتمان 85 متری سعادت‌آباد',
            created_by=self.user
        )
        
        response = self.client_api.get('/api/v1/properties/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(len(response.data['data']), 1)

    def test_retrieve_property(self):
        prop = Property.objects.create(
            code='AP-1001',
            title='آپارتمان 85 متری سعادت‌آباد',
            created_by=self.user
        )
        
        response = self.client_api.get(f'/api/v1/properties/{prop.public_id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['title'], 'آپارتمان 85 متری سعادت‌آباد')

    def test_update_property(self):
        prop = Property.objects.create(
            code='AP-1001',
            title='آپارتمان 85 متری سعادت‌آباد',
            created_by=self.user
        )
        
        response = self.client_api.patch(f'/api/v1/properties/{prop.public_id}/', {
            'title': 'آپارتمان 85 متری سعادت‌آباد - ویرایش شده'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        
        prop.refresh_from_db()
        self.assertEqual(prop.title, 'آپارتمان 85 متری سعادت‌آباد - ویرایش شده')

    def test_delete_property(self):
        prop = Property.objects.create(
            code='AP-1001',
            title='آپارتمان 85 متری سعادت‌آباد',
            created_by=self.user
        )
        
        response = self.client_api.delete(f'/api/v1/properties/{prop.public_id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        
        prop.refresh_from_db()
        self.assertTrue(prop.is_deleted)

    def test_duplicate_code_validation(self):
        Property.objects.create(
            code='AP-1001',
            title='آپارتمان 85 متری سعادت‌آباد',
            created_by=self.user
        )
        
        response = self.client_api.post('/api/v1/properties/', {
            'code': 'AP-1001',
            'title': 'آپارتمان دیگر',
            'property_type': 'آپارتمان',
            'listing_type': 'فروش'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
