from rest_framework import serializers

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


class BrandSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = ["name", "slug", "description", "products"]


class CategorySerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["name", "slug", "description", "products"]


class ProductDetailSerializer(serializers.ModelSerializer):
    brand = BrandListSerializer(read_only=True)
    category = CategoryListSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["name", "slug", "selling_price", "brand", "category", "description"]
