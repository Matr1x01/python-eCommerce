from django.db.models import Model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from .models import Product, Brand, Category
from .serializers import ProductListSerializer, ProductDetailSerializer, BrandListSerializer, BrandSerializer, \
    CategoryListSerializer, CategorySerializer


class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductListSerializer(products, many=True)
        return Response({"products": serializer.data}, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    def get(self, request, slug):
        try:
            product = Product.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductDetailSerializer(product)
        return Response({"product": serializer.data}, status=status.HTTP_200_OK)


class BrandListView(APIView):
    def get(self, request):
        brands = Brand.objects.all()
        serializer = BrandListSerializer(brands, many=True)
        return Response({"brands": serializer.data}, status=status.HTTP_200_OK)


class BrandDetailView(APIView):
    def get(self, request, slug):
        try:
            brand = Brand.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return Response({"error": "Brand not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BrandSerializer(brand)
        return Response({"brand": serializer.data}, status=status.HTTP_200_OK)


class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategoryListSerializer(categories, many=True)
        return Response({"categories": serializer.data}, status=status.HTTP_200_OK)


class CategoryDetailView(APIView):
    def get(self, request, slug):
        try:
            category = Category.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category)
        return Response({"category": serializer.data}, status=status.HTTP_200_OK)
