from django.urls import include, path

urlpatterns = [
    path('', include('product.urls')),
    path('', include('users.urls')),
    path('', include('address.urls')),
    path('', include('cart.urls')),
    path('', include('order.urls')), 
]
