from django.urls import path

from . import views

urlpatterns = [
    path("products/", views.ProductListView.as_view(http_method_names=['get']), name="products"),
    path("products/<slug>/", views.ProductDetailView.as_view(http_method_names=['get']), name="product-detail"),
    path("brands/", views.BrandListView.as_view(http_method_names=['get']), name="brands"),
    path("brands/<slug>/", views.BrandDetailView.as_view(http_method_names=['get']), name="brand-detail"),
    path("category/", views.CategoryListView.as_view(http_method_names=['get']), name="category"),
    path("category/<slug>/", views.CategoryDetailView.as_view(http_method_names=['get']), name="category-detail"),
]

