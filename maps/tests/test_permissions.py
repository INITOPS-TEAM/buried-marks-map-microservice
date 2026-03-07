from django.test import TestCase
from rest_framework.test import APIClient
from maps.models import MapPoint, ArtifactCategory
from unittest.mock import patch
from maps.middleware import JWTMiddleware
from maps.tests.utils import make_jwt_mock


class PermissionsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = ArtifactCategory.objects.create(name='scout')
        self.marker = MapPoint.objects.create(
            label='Test Marker',
            category=self.category,
            lat='50.456901450626360000',
            lng='30.426901450626360010',
            description='Test description',
            author_id=1
        )
        self.client.credentials(HTTP_AUTHORIZATION='Bearer test_token')

    @patch.object(JWTMiddleware, '__call__', autospec=True)
    def test_viewer_can_list_markers(self, mock_jwt):
        mock_jwt.side_effect = make_jwt_mock('1')

        response = self.client.get('/api/markers/')
        print(f'\n[test_viewer_can_list_markers] status: {response.status_code}')
        self.assertEqual(response.status_code, 200)

    @patch.object(JWTMiddleware, '__call__', autospec=True)
    def test_viewer_cannot_create_marker(self, mock_jwt):
        mock_jwt.side_effect = make_jwt_mock('1')

        response = self.client.post('/api/markers/', {
            'label': 'Test Marker',
            'category': 'scout',
            'lat': '50.416901450626360000',
            'lng': '30.563747823436955000',
            'author_id': 1,
            'description': 'Test Marker'
        })
        print(f'\n[test_viewer_cannot_create_marker] status: {response.status_code}')
        self.assertEqual(response.status_code, 403)

    @patch.object(JWTMiddleware, '__call__', autospec=True)
    def test_editor_can_create_marker(self, mock_jwt):
        mock_jwt.side_effect = make_jwt_mock('2')

        response = self.client.post('/api/markers/', {
            'label': 'Test Marker',
            'category': 'scout',
            'lat': '50.416901450626360000',
            'lng': '30.563747823436955000',
            'author_id': 1,
            'description': 'Test Marker'
        })
        print(f'\n[test_editor_can_create_marker] status: {response.status_code}')
        self.assertEqual(response.status_code, 201)

    @patch.object(JWTMiddleware, '__call__', autospec=True)
    def test_viewer_cannot_delete_marker(self, mock_jwt):
        mock_jwt.side_effect = make_jwt_mock('1')

        response = self.client.delete(f'/api/markers/{self.marker.id}/')
        print(f'\n[test_viewer_cannot_delete_marker] status: {response.status_code}')
        self.assertEqual(response.status_code, 403)

    @patch.object(JWTMiddleware, '__call__', autospec=True)
    def test_admin_can_delete_marker(self, mock_jwt):
        mock_jwt.side_effect = make_jwt_mock('3')

        response = self.client.delete(f'/api/markers/{self.marker.id}/')
        print(f'\n[test_admin_can_delete_marker] status: {response.status_code}')
        self.assertEqual(response.status_code, 204)
