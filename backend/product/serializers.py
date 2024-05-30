from urllib.parse import urljoin
from rest_framework import serializers
from django.conf import settings
from .models import Product, Brand, Category


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
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        return urljoin(settings.APP_URL, obj.images.url) if obj.images else ''

    class Meta:
        model = Product
        fields = ["name", "slug", "selling_price", "brand", "category", "images"]


class BrandSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    def get_logo(self, obj):
        return urljoin(settings.APP_URL, obj.logo.url) if obj.logo else ''

    class Meta:
        model = Brand
        fields = ["name", "slug", "description", "logo"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "slug", "description"]


class ProductDetailSerializer(serializers.ModelSerializer):
    brand = BrandListSerializer(read_only=True)
    category = CategoryListSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["name", "slug", "selling_price", "brand", "category", "description"]
