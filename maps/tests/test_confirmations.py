from django.test import TestCase
from rest_framework.test import APIClient
from maps.models import MapPoint, ArtifactCategory, Confirmation
from unittest.mock import patch
from maps.middleware import JWTMiddleware
from maps.tests.utils import make_jwt_mock, create_test_marker


class ConfirmationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = ArtifactCategory.objects.create(name='scout')
        self.marker = create_test_marker(self.category)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer test_token')

    @patch.object(JWTMiddleware, '__call__', autospec=True)
    def test_confirm_marker(self, mock_jwt):
        mock_jwt.side_effect = make_jwt_mock('1')

        response = self.client.post(f'/api/markers/{self.marker.id}/confirm/')
        print(f'\n[test_confirm_marker] status: {response.status_code}, confirmations: {Confirmation.objects.count()}')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Confirmation.objects.count(), 1)

    @patch.object(JWTMiddleware, '__call__', autospec=True)
    def test_cannot_confirm_own_marker(self, mock_jwt):
        mock_jwt.side_effect = make_jwt_mock('1')

        own_marker = create_test_marker(self.category, author_id=1)

        response = self.client.post(f'/api/markers/{own_marker.id}/confirm/')
        print(f'\n[test_cannot_confirm_own_marker] status: {response.status_code}')
        self.assertEqual(response.status_code, 400)

    @patch.object(JWTMiddleware, '__call__', autospec=True)
    def test_unconfirm_marker(self, mock_jwt):
        mock_jwt.side_effect = make_jwt_mock('1')

        Confirmation.objects.create(marker=self.marker, author_id=1)

        response = self.client.delete(f'/api/markers/{self.marker.id}/confirm/')
        print(f'\n[test_unconfirm_marker] status: {response.status_code}, confirmations: {Confirmation.objects.count()}')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Confirmation.objects.count(), 0)

    @patch.object(JWTMiddleware, '__call__', autospec=True)
    def test_confirm_count_in_marker_list(self, mock_jwt):
        mock_jwt.side_effect = make_jwt_mock('1')

        Confirmation.objects.create(marker=self.marker, author_id=1)

        response = self.client.get('/api/markers/')
        print(f'\n[test_confirm_count_in_marker_list] status: {response.status_code}, confirm_count: {response.data[0]["confirm_count"]}, confirmed_by_me: {response.data[0]["confirmed_by_me"]}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['confirm_count'], 1)
        self.assertTrue(response.data[0]['confirmed_by_me'])
