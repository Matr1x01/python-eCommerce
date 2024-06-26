from rest_framework import serializers

from .models import Coupon


class ApplyCouponSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = Coupon
        fields = ['code']
        read_only_fields = fields
