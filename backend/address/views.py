from rest_framework.views import APIView
from backend.utils.Responder import Responder
from .serializers import AddressSerializer
from rest_framework import status
from .models import Address
from backend.utils.ParseError import parse_error


class AddressView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            addresses = request.user.customer.addresses.all()
            serializer = AddressSerializer(addresses, many=True)
            return Responder.success_response('Addresses fetched successfully', serializer.data)
        return Responder.error_response('Unauthorized', status_code=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = AddressSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(customer=request.user.customer)
                return Responder.success_response('Address added successfully', serializer.data)
            return Responder.error_response('Invalid data', serializer.errors)
        return Responder.error_response('Unauthorized', status_code=status.HTTP_401_UNAUTHORIZED)


class AddressDetailView(APIView):
    def get(self, request, uuid):
        if request.user.is_authenticated:
            try:
                address = request.user.customer.addresses.get(uuid=uuid)
            except Exception as e:
                return Responder.error_response(message='Address not found', errors=parse_error(e), status_code=status.HTTP_404_NOT_FOUND)
            serializer = AddressSerializer(address)
            return Responder.success_response('Address fetched successfully', serializer.data)
        return Responder.error_response('Unauthorized', status_code=status.HTTP_401_UNAUTHORIZED)


class AddressUpdateView(APIView):
    def put(self, request, uuid):
        if request.user.is_authenticated:
            try:
                address = request.user.customer.addresses.get(uuid=uuid)
            except Address.DoesNotExist:
                return Responder.error_response('Address not found', status_code=status.HTTP_404_NOT_FOUND)
            serializer = AddressSerializer(address, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Responder.success_response('Address updated successfully', serializer.data)
            return Responder.error_response('Invalid data', serializer.errors)
        return Responder.error_response('Unauthorized', status_code=status.HTTP_401_UNAUTHORIZED)
