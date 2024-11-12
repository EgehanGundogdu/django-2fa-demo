# users/middleware.py


class OtpVerifiedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            is_verified = request.session.get("is_verified", False)
            request.user.is_verified = is_verified

        response = self.get_response(request)
        return response
