from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "slug", "cost_price", "selling_price", "description", "brand", "created_at", "updated_at"]