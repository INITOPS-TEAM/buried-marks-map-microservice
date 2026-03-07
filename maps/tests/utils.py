from maps.middleware import JWTMiddleware
from maps.models import MapPoint

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

TEST_MARKER_POST_DATA = {
    'label': 'Test Marker',
    'category': 'scout',
    'lat': '50.416901450626360000',
    'lng': '30.563747823436955000',
    'author_id': 1,
    'description': 'Test Marker'
}
