from django.http import JsonResponse,HttpResponse


def index(request:HttpResponse):
    print(request.headers)
    return JsonResponse(
        {"message": "Hello, world. You're at the product index."},
        status=200,
        content_type="json/application"
    )