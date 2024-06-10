from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from product.models import Product, Category, Brand


# path("products/",
#      views.ProductListView.as_view(http_method_names=['get']), name="products"),
# path("products/<slug>/", views.ProductDetailView.as_view(
#     http_method_names=['get']), name="product-detail"),
# path("brands/",
#      views.BrandListView.as_view(http_method_names=['get']), name="brands"),
# path("brands/<slug>/",
#      views.BrandDetailView.as_view(http_method_names=['get']), name="brand-detail"),
# path("category/",
#      views.CategoryListView.as_view(http_method_names=['get']), name="category"),
# path("category/<slug>/", views.CategoryDetailView.as_view(
#     http_method_names=['get']), name="category-detail"),

class ProductTests(APITestCase):
    def test_get_products(self):
        url = reverse('products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
