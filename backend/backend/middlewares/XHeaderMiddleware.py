from django.http import JsonResponse
from rest_framework.status import HTTP_400_BAD_REQUEST


class XHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        headers = request.headers
        if 'X-Requested-With' in headers and headers['X-Requested-With'] == 'XMLHttpRequest':
            return self.get_response(request)
        return JsonResponse({'error': 'X-Requested-With must be XMLHttpRequest'}, status=HTTP_400_BAD_REQUEST)
