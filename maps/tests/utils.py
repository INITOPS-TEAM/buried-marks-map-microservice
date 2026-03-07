from maps.middleware import JWTMiddleware

def make_jwt_mock(role='2'):
    def fake_call(middleware, request):
        request.user_id = 1
        request.user_role = role
        return middleware.get_response(request)
    return fake_call
