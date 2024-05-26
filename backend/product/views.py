from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Brand, Category
from .serializers import ProductSerializer


class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({"products": serializer.data}, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    def get(self, request, id: int):
        product = Product.objects.get(id=id)
        print(product)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response({"product": serializer.data}, status=status.HTTP_200_OK)
