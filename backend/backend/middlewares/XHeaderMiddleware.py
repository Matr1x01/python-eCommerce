from django.http import JsonResponse
from rest_framework.status import HTTP_400_BAD_REQUEST


class XHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        headers = request.headers
        response = self.get_response(request)

        if not request.path.startswith('/api/'):
            return response

        if 'X-Requested-With' in headers and headers['X-Requested-With'] == 'XMLHttpRequest':
            return response

        return JsonResponse({'error': 'X-Requested-With must be XMLHttpRequest'}, status=HTTP_400_BAD_REQUEST)
