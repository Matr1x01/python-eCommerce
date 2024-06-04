from django.urls import include, path

urlpatterns = [
    path('', include('product.urls')),
    path('', include('users.urls')),
    path('', include('address.urls')),
]
