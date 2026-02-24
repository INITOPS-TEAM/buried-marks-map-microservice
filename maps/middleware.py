import jwt
from django.conf import settings

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        request.user_id = None
        request.user_role = None

        if token:
            try:
                payload = jwt.decode(token, settings.JWT_PUBLIC_KEY, algorithms=['ES256'])
                request.user_id = payload.get('user_id')
                request.user_role = payload.get('role')

            except jwt.ExpiredSignatureError:
                pass
            except jwt.InvalidTokenError:
                pass

        return self.get_response(request)
