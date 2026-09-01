from django.http import JsonResponse
from api.exceptions import ApplicationError

class ApplicationErrorMiddleware:
    """Middleware to handle ApplicationError exceptions globally."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except ApplicationError as e:
            return JsonResponse({"error": e.message}, status=e.status_code)