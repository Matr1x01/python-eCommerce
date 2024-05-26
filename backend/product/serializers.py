from rest_framework import serializers

from .models import Product


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "slug","selling_price", "brand","category"]

class ProductDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "selling_price", "brand","category","description"]