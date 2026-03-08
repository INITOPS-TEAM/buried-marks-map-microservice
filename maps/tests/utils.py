from django.test import TestCase
from maps.middleware import JWTMiddleware
from rest_framework.test import APIClient
from maps.models import MapPoint, ArtifactCategory

def make_jwt_mock(role='2'):
    def fake_call(middleware, request):
        request.user_id = 1
        request.user_role = role
        return middleware.get_response(request)
    return fake_call

def create_test_marker(category, author_id=2):
    return MapPoint.objects.create(
        label='Test Marker',
        category=category,
        lat='50.456901450626360000',
        lng='30.426901450626360010',
        description='Test description',
        author_id=author_id
    )

class BaseMarkerTestCase(TestCase):
    """Base test case with common setup."""
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.category = ArtifactCategory.objects.create(name='scout')
        self.marker = create_test_marker(self.category)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer test_token')

TEST_MARKER_POST_DATA = {
    'label': 'Test Marker',
    'category': 'scout',
    'lat': '50.416901450626360000',
    'lng': '30.563747823436955000',
    'author_id': 1,
    'description': 'Test Marker'
}
