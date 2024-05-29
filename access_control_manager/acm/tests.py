from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import GroupPermissions
from django.contrib.auth import get_user_model
from django.conf import settings
User = get_user_model()

settings.DEBUG = True
class GroupPermissionsCRUDTests(TestCase):
    def setUp(self):
        # Create a test user for authentication
        self.user = User.objects.create_user(
            password='testpassword',
            user_number="09122222222"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create a test group permission for existing data
        self.group_permission = GroupPermissions.objects.create(
            name='Test Group',
            permission_type='model',
            permission_key='model_read',
            extra_fields={
                "model_name": "TestModel",
                "access": [
                    "READ",
                    "CREATE",
                    "UPDATE",
                    "DELETE"
                ]
            }
        )

        # URL for the GroupPermissionsViewSet
        self.url = '/acm/group-permissions/'  # Replace with your actual URL

    def test_create_group_permission(self):
        data = {
            'name': 'New Group',
            'permission_type': 'model',
            'permission_key': 'model_perm',
            'extra_fields': {
                "model_name": "TestModel",
                "access": [
                    "READ",
                    "CREATE",
                    "UPDATE",
                    "DELETE"
                ]
            }
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('id' in response.data)
        self.assertEqual(response.data['name'], data['name'])

    def test_read_group_permission_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result= response.data.get('results') if 'results' in response.data else response.data
        self.assertEqual(len(result), GroupPermissions.objects.count())

    def test_read_group_permission_detail(self):
        response = self.client.get(f'{self.url}{self.group_permission.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.group_permission.id)
        self.assertEqual(response.data['name'], self.group_permission.name)

    def test_update_group_permission(self):
        data = {
            'name': 'Updated Group',
            'permission_type': self.group_permission.permission_type,
            'permission_key': self.group_permission.permission_key,
            'extra_fields': self.group_permission.extra_fields
        }
        response = self.client.put(f'{self.url}{self.group_permission.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.group_permission.id)
        self.assertEqual(response.data['name'], data['name'])

    def test_partial_update_group_permission(self):
        data = {'permission_type': "endpoint", "extra_fields": {"url": "http://example.com", "method":"POST"}}
        response = self.client.patch(f'{self.url}{self.group_permission.id}/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.group_permission.id)
        self.assertEqual(response.data['permission_type'], data['permission_type'])

    def test_delete_group_permission(self):
        response = self.client.delete(f'{self.url}{self.group_permission.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(GroupPermissions.DoesNotExist):
            GroupPermissions.objects.get(id=self.group_permission.id)
