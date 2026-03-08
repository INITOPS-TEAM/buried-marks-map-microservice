from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from maps.models import MapPoint, ArtifactCategory
from unittest.mock import patch
from moto import mock_aws
from maps.middleware import JWTMiddleware
from maps.tests.utils import make_jwt_mock, create_test_marker, TEST_MARKER_POST_DATA
import boto3
import os


class MarkerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = ArtifactCategory.objects.create(name='scout')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer test_token')

    @patch.object(JWTMiddleware, '__call__', autospec=True)
    def test_create_marker(self, mock_jwt):
        mock_jwt.side_effect = make_jwt_mock('2')

        response = self.client.post('/api/markers/', TEST_MARKER_POST_DATA)

        print(f'\n[test_create_marker] status: {response.status_code}, data: {response.data}')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(MapPoint.objects.count(), 1)

    @patch.object(JWTMiddleware, '__call__', autospec=True)
    def test_list_markers(self, mock_jwt):
        mock_jwt.side_effect = make_jwt_mock('1')

        create_test_marker(self.category)

        response = self.client.get('/api/markers/')
        print(f'\n[test_list_markers] status: {response.status_code}, count: {len(response.data)}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    @mock_aws
    @patch.object(JWTMiddleware, '__call__', autospec=True)
    def test_create_and_delete_marker_with_image(self, mock_jwt):
        os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
        os.environ['AWS_STORAGE_BUCKET_NAME'] = 'buried-marks-media'

        s3 = boto3.client('s3', region_name='eu-north-1')
        s3.create_bucket(
            Bucket='buried-marks-media',
            CreateBucketConfiguration={'LocationConstraint': 'eu-north-1'}
        )

        mock_jwt.side_effect = make_jwt_mock('3')


        image_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'test.jpg')
        with open(image_path, 'rb') as f:
            image = SimpleUploadedFile('test.jpg', f.read(), content_type='image/jpeg')

        count = MapPoint.objects.count()
        print(f'\n[test_create_and_delete_marker_with_image] markers before: {count}')

        response = self.client.post('/api/markers/', TEST_MARKER_POST_DATA)

        print(f'[test_create_and_delete_marker_with_image] create status: {response.status_code}, data: {response.data}')
        self.assertEqual(response.status_code, 201)
        marker_id = response.data['id']

        delete_response = self.client.delete(f'/api/markers/{marker_id}/')
        print(f'[test_create_and_delete_marker_with_image] delete status: {delete_response.status_code}')
        self.assertEqual(delete_response.status_code, 204)
        self.assertEqual(MapPoint.objects.count(), 0)
