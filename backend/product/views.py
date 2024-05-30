from rest_framework import status
from rest_framework.views import APIView
from .models import Product, Brand, Category
from .serializers import (
    ProductListSerializer, ProductDetailSerializer,
    BrandListSerializer, BrandSerializer,
    CategoryListSerializer, CategorySerializer
)
from backend.utils.Responder import Responder
from backend.utils.PaginatedAPIWiew import PaginatedAPIView


class ProductListView(PaginatedAPIView):
    def get(self, request):
        products = Product.objects.defer('description', 'cost_price').order_by('name')
        products = self.get_paginated_response(products, ProductListSerializer)
        return Responder.success_response('Products fetched successfully', products)


class ProductDetailView(APIView):
    def get(self, request, slug):
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return Responder.error_response('Product not found', status.HTTP_404_NOT_FOUND)

        serializer = ProductDetailSerializer(product)
        return Responder.success_response('Product fetched successfully', {'product': serializer.data})


class BrandListView(PaginatedAPIView):
    def get(self, request):
        brands = Brand.objects.order_by('name')
        brands = self.get_paginated_response(brands, BrandListSerializer)
        return Responder.success_response('Brands fetched successfully', brands)


class BrandDetailView(PaginatedAPIView):
    def get(self, request, slug):
        try:
            brand = Brand.objects.get(slug=slug)
        except Brand.DoesNotExist:
            return Responder.error_response('Brand not found', status.HTTP_404_NOT_FOUND)

        brand_serializer = BrandSerializer(brand)
        products = Product.objects.filter(brand=brand).order_by('name')
        paginated_products_response = self.get_paginated_response(products, ProductListSerializer)
        print(paginated_products_response)

        return Responder.success_response('Brand fetched successfully', {
            'brand': brand_serializer.data,
            'products': paginated_products_response['items'],
            'meta': paginated_products_response['meta']
        })


class CategoryListView(PaginatedAPIView):
    def get(self, request):
        categories = Category.objects.order_by('name')
        categories = self.get_paginated_response(categories, CategoryListSerializer)
        return Responder.success_response('Categories fetched successfully', categories)


class CategoryDetailView(PaginatedAPIView):
    def get(self, request, slug):
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return Responder.error_response('Category not found', status.HTTP_404_NOT_FOUND)

        category_serializer = CategorySerializer(category)
        products = Product.objects.filter(category=category).order_by('name')
        paginated_products_response = self.get_paginated_response(products, ProductListSerializer)

        return Responder.success_response('Category fetched successfully', {
            'category': category_serializer.data,
            'products': paginated_products_response['items'],
            'meta': paginated_products_response['meta']
        })
