from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from apps.clients.models import Client
from apps.properties.models import Property
from apps.sales.models import Deal, Pipeline, Stage

User = get_user_model()


class DealCRUDTests(TestCase):
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
        
        self.pipeline = Pipeline.objects.create(
            name='پایپ‌لاین فروش مسکونی',
            is_active=True
        )
        
        self.stage1 = Stage.objects.create(
            pipeline=self.pipeline,
            name='لید جدید',
            sort_order=1
        )
        
        self.stage2 = Stage.objects.create(
            pipeline=self.pipeline,
            name='تماس اولیه',
            sort_order=2
        )
        
        self.client_obj = Client.objects.create(
            full_name='علی رضایی',
            phone='09121111111',
            created_by=self.user
        )
        
        self.property_obj = Property.objects.create(
            code='AP-1001',
            title='آپارتمان 85 متری سعادت‌آباد',
            created_by=self.user
        )

    def test_create_deal(self):
        response = self.client_api.post('/api/v1/deals/', {
            'title': 'خرید آپارتمان سعادت‌آباد',
            'client': str(self.client_obj.public_id),
            'property': str(self.property_obj.public_id),
            'pipeline': str(self.pipeline.public_id),
            'stage': str(self.stage1.public_id),
            'amount': 7000000000,
            'probability': 60,
            'status': 'Open'
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(Deal.objects.count(), 1)

    def test_list_deals(self):
        Deal.objects.create(
            title='خرید آپارتمان سعادت‌آباد',
            client=self.client_obj,
            property=self.property_obj,
            pipeline=self.pipeline,
            stage=self.stage1,
            amount=7000000000,
            created_by=self.user
        )
        
        response = self.client_api.get('/api/v1/deals/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(len(response.data['data']), 1)

    def test_move_deal(self):
        deal = Deal.objects.create(
            title='خرید آپارتمان سعادت‌آباد',
            client=self.client_obj,
            property=self.property_obj,
            pipeline=self.pipeline,
            stage=self.stage1,
            amount=7000000000,
            created_by=self.user
        )
        
        response = self.client_api.post(f'/api/v1/deals/{deal.public_id}/move/', {
            'stage': str(self.stage2.public_id)
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        
        deal.refresh_from_db()
        self.assertEqual(deal.stage, self.stage2)

    def test_move_deal_to_different_pipeline_stage(self):
        deal = Deal.objects.create(
            title='خرید آپارتمان سعادت‌آباد',
            client=self.client_obj,
            property=self.property_obj,
            pipeline=self.pipeline,
            stage=self.stage1,
            amount=7000000000,
            created_by=self.user
        )
        
        pipeline2 = Pipeline.objects.create(
            name='پایپ‌لاین فروش تجاری',
            is_active=True
        )
        
        stage_other = Stage.objects.create(
            pipeline=pipeline2,
            name='مرحله دیگر',
            sort_order=1
        )
        
        response = self.client_api.post(f'/api/v1/deals/{deal.public_id}/move/', {
            'stage': str(stage_other.public_id)
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
