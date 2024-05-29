from urllib.parse import urljoin

from rest_framework import serializers
from django.core.paginator import Paginator
from .models import *
from django.conf import settings


class BrandListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ["name", "slug"]
        read_only_fields = ["name", "slug"]


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "slug"]
        read_only_fields = ["name", "slug"]


class ProductListSerializer(serializers.ModelSerializer):
    brand = BrandListSerializer(read_only=True)
    category = CategoryListSerializer(many=True, read_only=True)
    images = serializers.SerializerMethodField("get_images")

    def get_images(self, obj):
        if obj.images:
            return urljoin(settings.APP_URL, obj.images.url)
        return ''

    class Meta:
        model = Product
        fields = ["name", "slug", "selling_price", "brand", "category", "images"]
        read_only_fields = ["name", "slug", "selling_price", "brand", "category", "images"]


def _paginated_products(self, obj):
    products = obj.products.all().order_by('name')
    paginator = Paginator(
        products, self.context["request"].GET.get("per_page", 10))
    page = paginator.page(self.context["request"].GET.get("page", 1))
    serializer = ProductListSerializer(page, many=True)
    return serializer.data


class BrandSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField("paginated_products")
    logo = serializers.SerializerMethodField("get_logo")

    def get_logo(self, obj):
        if obj.logo:
            return urljoin(settings.APP_URL, obj.logo.url)
        return ''

    class Meta:
        model = Brand
        fields = ["name", "slug", "description", "products", "logo"]
        read_only_fields = ["name", "slug", "description", "products", "logo"]

    def paginated_products(self, obj):
        return _paginated_products(self, obj)


class CategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField("paginated_products")

    class Meta:
        model = Category
        fields = ["name", "slug", "description", "products"]
        read_only_fields = ["name", "slug", "description", "products"]

    def paginated_products(self, obj):
        return _paginated_products(self, obj)


class ProductDetailSerializer(serializers.ModelSerializer):
    brand = BrandListSerializer(read_only=True)
    category = CategoryListSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["name", "slug", "selling_price",
                  "brand", "category", "description"]
        read_only_fields = ["name", "slug", "selling_price",
                            "brand", "category", "description"]
