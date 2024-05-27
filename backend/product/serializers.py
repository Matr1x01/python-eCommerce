from rest_framework import serializers,pagination
from django.core.paginator import Paginator
from .models import *


class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["name", "slug"]


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "slug"]


class ProductListSerializer(serializers.ModelSerializer):
    brand = BrandListSerializer(read_only=True)
    category = CategoryListSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["name", "slug", "selling_price", "brand", "category"]
 

def _paginated_products(self, obj):
        products = obj.products.all()
        paginator = Paginator(products, self.context["request"].GET.get("per_page", 10))
        page = paginator.page(self.context["request"].GET.get("page", 1))
        serializer = ProductListSerializer(page, many=True)
        return serializer.data

class BrandSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField("paginated_products")

    class Meta:
        model = Brand
        fields = ["name", "slug", "description", "products"]
    
    def paginated_products(self, obj):
        return _paginated_products(self, obj)


class CategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField("paginated_products")

    class Meta:
        model = Category
        fields = ["name", "slug", "description", "products"]

    def paginated_products(self, obj):
        return _paginated_products(self, obj)


class ProductDetailSerializer(serializers.ModelSerializer):
    brand = BrandListSerializer(read_only=True)
    category = CategoryListSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["name", "slug", "selling_price", "brand", "category", "description"]
