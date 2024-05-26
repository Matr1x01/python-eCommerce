from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProductListView.as_view(http_method_names=['get']), name="index"),
    path("<int:id>/", views.ProductDetailView.as_view(http_method_names=['get']), name="detail"),
]
