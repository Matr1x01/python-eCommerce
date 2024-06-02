import re
from rest_framework import serializers
from .models import Customer


def validate_phone(phone):
    phone = phone.strip()
    pattern = r"^01[1-9]\d{8}$"
    if phone.startswith('88'):
        phone = phone[2:]
    if not re.match(pattern, phone):
        raise serializers.ValidationError("Phone number format is invalid")
    return phone


class CustomerRegisterSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    phone = serializers.CharField(max_length=15, min_length=11, required=True)
    password = serializers.CharField(max_length=255, min_length=8, required=True, write_only=True)
    confirm_password = serializers.CharField(max_length=255, min_length=8, required=True, write_only=True)
    date_of_birth = serializers.DateField(required=False)
    gender = serializers.CharField(required=False)

    def validate(self, data):
        data['phone'] = validate_phone(data['phone'])

        # validate password and confirm password
        password = data['password']
        confirm_password = data['confirm_password']
        if password != confirm_password:
            raise serializers.ValidationError("Password and confirm password does not match")
        del data['confirm_password']
        self.password = password
        del data['password']
        return data

    def create(self, validated_data):
        customer = Customer.objects.create(**validated_data)
        customer.user.set_password(self.password)
        customer.user.save()
        return customer

    class Meta:
        model = Customer
        fields = ('name', 'phone', 'date_of_birth', 'gender')


class CustomerLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, min_length=11, required=True)
    password = serializers.CharField(max_length=255, min_length=8, required=True, write_only=True)

    def validate(self, data):
        data['phone'] = validate_phone(data['phone'])
        return data

    class Meta:
        model = Customer
        fields = ('phone', 'password')
        extra_kwargs = {
            'password': {'write_only': True, 'hidden': True}
        }
