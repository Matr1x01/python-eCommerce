from django.urls import path
from .views import CartAPIView, WishlistAPIView, CartAddressAPIView

urlpatterns = [
    path('cart/', CartAPIView.as_view(http_method_names=['get', 'post', 'delete']), name='cart'),
    path('cart/address/', CartAddressAPIView.as_view(http_method_names=['post']), name='cart_address'),
    path('wishlist/', WishlistAPIView.as_view(http_method_names=['get', 'post', 'delete']), name='wishlist'),
]