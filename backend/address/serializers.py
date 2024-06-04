from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ['address', 'uuid', 'area', 'city', 'state', 'country', 'postal_code']
        read_only_fields = ['uuid']