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
    image = serializers.SerializerMethodField()
    selling_price = serializers.SerializerMethodField()

    def get_selling_price(self, obj):
        return float(obj.selling_price)

    def get_image(self, obj):
        return urljoin(settings.APP_URL, obj.first_image.image.url) if obj.first_image else ''

    class Meta:
        model = Product
        fields = ["name", "slug", "selling_price", "brand", "category", "image"]


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
    selling_price = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        return [urljoin(settings.APP_URL, image.image.url) for image in obj.images]

    def get_selling_price(self, obj):
        return float(obj.selling_price)

    class Meta:
        model = Product
        fields = ["name", "slug", "selling_price", "brand", "category", "description", "images"]
