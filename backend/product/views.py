from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Brand, Category
from product.serializers import ProductListSerializer, ProductDetailSerializer


class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductListSerializer(products, many=True)
        return Response({"products": serializer.data}, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    def get(self, request, id: int):
        product = Product.objects.get(id=id)
        print(product)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductDetailSerializer(product)
        return Response({"product": serializer.data}, status=status.HTTP_200_OK)
