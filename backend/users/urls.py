from django.urls import path
from . import views

urlpatterns = [
    path('register', views.CustomerRegisterView.as_view(http_method_names=['post']), name='register',),
    path('login', views.CustomerLoginView.as_view(http_method_names=['post']), name='login',),
    path('profile', views.CustomerDetailView.as_view(http_method_names=['get']), name='customer-detail',),
    path('profile/update', views.CustomerDetailView.as_view(http_method_names=['put']), name='customer-update',),
    path('password/update', views.CustomerPasswordUpdateView.as_view(http_method_names=['put']), name='password-update',),
]