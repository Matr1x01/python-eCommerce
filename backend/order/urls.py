from django.urls import path

from order.views import OrderAPIView

urlpatterns = [
    path('order/', OrderAPIView.as_view(http_method_names=['get', 'post', 'delete']), name='order'),
    path('order/<str:key>/', OrderDetailsAPIView.as_view(http_method_names=['get']), name='order-detail'),
 ]