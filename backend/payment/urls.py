from django.urls import path
from .views import PaymentAPIView

urlpatterns = [
    path('make-payment/', PaymentAPIView.as_view(http_method_names=['get', 'post']), name='make-payment'),
 ]