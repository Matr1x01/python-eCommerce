from django.urls import path
from .views import CartAPIView, WishlistAPIView

urlpatterns = [
    path('cart/', CartAPIView.as_view(http_method_names=['get', 'post', 'delete']), name='cart'),
    path('wishlist/', WishlistAPIView.as_view(http_method_names=['get', 'post', 'delete']), name='wishlist'),
]