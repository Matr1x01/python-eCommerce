from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from .models import Product, Brand, Category
from .serializers import ProductListSerializer, ProductDetailSerializer, BrandListSerializer, BrandSerializer, \
    CategoryListSerializer, CategorySerializer
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from backend.utils.Responder import Responder

class ProductListView(APIView):
    def get(self, request): 
        per_page = request.GET.get('per_page', 10)
        current_page = request.GET.get('page', 1)
        products = Product.objects.defer('description','cost_price').all()
        paginator = Paginator(products, per_page)
        try :
            products=paginator.page(current_page)
        except EmptyPage:
            return Responder.success_response('No products found',{'products':{}},status.HTTP_404_NOT_FOUND)
        serializer = ProductListSerializer(products, many=True)
        return Responder.success_response('Products fetched successfully',{'products':serializer.data})


class ProductDetailView(APIView):
    def get(self, request, slug):
        try:
            product = Product.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return Responder.error_response('Product not found',status.HTTP_404_NOT_FOUND)

        serializer = ProductDetailSerializer(product)
        return Responder.success_response('Product fetched successfully',{'product':serializer.data})


class BrandListView(APIView):
    def get(self, request):
        per_page = request.GET.get('per_page', 10)
        current_page = request.GET.get('page', 1)
        brands = Brand.objects.all()
        paginator = Paginator(brands, per_page)
        try :
            brands=paginator.page(current_page)
        except EmptyPage:
            return Responder.success_response('No brands found',{'brands':{}},status.HTTP_404_NOT_FOUND)
        serializer = BrandListSerializer(brands, many=True)
        return Responder.success_response('Brands fetched successfully',{'brands':serializer.data})


class BrandDetailView(APIView):
    def get(self, request, slug):
        try:
            brand = Brand.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return Response({"error": "Brand not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BrandSerializer(brand, context={'request': request})
        return Responder.success_response('Brand fetched successfully',{'brand':serializer.data})


class CategoryListView(APIView):
    def get(self, request):
        per_page = request.GET.get('per_page', 10)
        current_page = request.GET.get('page', 1)
        categories = Category.objects.all()
        paginator = Paginator(categories, per_page)
        try :
            categories=paginator.page(current_page)
        except EmptyPage:
            return Responder.success_response('No categories found',{'categories':{}},status.HTTP_404_NOT_FOUND) 
        serializer = CategoryListSerializer(categories, many=True)
        return Responder.success_response('Categories fetched successfully',{'categories':serializer.data})


class CategoryDetailView(APIView):
    def get(self, request, slug):
        try:
            category = Category.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return Responder.error_response('Category not found',status.HTTP_404_NOT_FOUND) 
        serializer = CategorySerializer(category, context={'request': request})
        return Responder.success_response('Category fetched successfully',{'category':serializer.data})
