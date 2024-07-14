from urllib.parse import urljoin
from rest_framework import serializers
from django.conf import settings
from .models import Product, Brand, Category


class BrandListSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    def get_logo(self, obj):
        return urljoin(settings.APP_URL, obj.logo.url) if obj.logo else ''

    class Meta:
        model = Brand
        fields = ["name", "slug", "logo"]


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "slug"]


class ProductListSerializer(serializers.ModelSerializer):
    brand = BrandListSerializer(read_only=True)
    category = CategoryListSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()
    selling_price = serializers.SerializerMethodField()
    has_discount = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField()

    def get_selling_price(self, obj):
        return float(obj.selling_price)

    def get_has_discount(self, obj):
        return obj.discount_price is not None and obj.discount_price > 0

    def get_discount_price(self, obj):
        return float(obj.discount_price) if obj.discount_price else 0

    def get_image(self, obj):
        return urljoin(settings.APP_URL, obj.first_image.image.url) if obj.first_image else ''

    class Meta:
        model = Product
        fields = ["name", "slug", "selling_price", "brand", "category", "image", "has_discount", "discount_price"]


class ProductSearchSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    slug = serializers.CharField()

    class Meta:
        model = Product
        fields = ["name", "slug"]


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
    has_discount = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        return [urljoin(settings.APP_URL, image.image.url) for image in obj.images]

    def get_selling_price(self, obj):
        return float(obj.selling_price)

    def get_has_discount(self, obj):
        return obj.discount_price is not None and obj.discount_price > 0

    def get_discount_price(self, obj):
        return float(obj.discount_price) if obj.discount_price else 0

    class Meta:
        model = Product
        fields = ["name", "slug", "selling_price", "brand", "category", "description", "images", "has_discount",
                  "discount_price"]
