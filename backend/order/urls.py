from django.urls import path

from order.views import OrderAPIView, OrderDetailsAPIView, OrderCancelAPIView

urlpatterns = [
    path('orders/', OrderAPIView.as_view(http_method_names=['get', 'post']), name='order'),
    path('orders/<str:key>/', OrderDetailsAPIView.as_view(http_method_names=['get']), name='order-detail'),
    path('order-cancel/<str:key>/', OrderCancelAPIView.as_view(http_method_names=['post']), name='order-cancel'),
 ]