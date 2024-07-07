from rest_framework.views import APIView
from backend.utils.Responder import Responder
from .serializers import AddressSerializer
from rest_framework import status
from .models import Address
from backend.utils.ParseError import parse_error
from rest_framework.permissions import IsAuthenticated


class AddressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = request.user.customer.addresses.all()
        serializer = AddressSerializer(addresses, many=True)
        return Responder.success_response('Addresses fetched successfully', serializer.data)

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=request.user.customer)
            return Responder.success_response('Address added successfully', serializer.data, status_code=status.HTTP_201_CREATED)
        return Responder.error_response('Invalid data', serializer.errors)


class AddressDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, uuid):
        try:
            address = request.user.customer.addresses.get(uuid=uuid)
        except Exception as e:
            return Responder.error_response(message='Address not found', errors=parse_error(e),
                                            status_code=status.HTTP_404_NOT_FOUND)
        serializer = AddressSerializer(address)
        return Responder.success_response('Address fetched successfully', serializer.data)

    def put(self, request, uuid):
        try:
            address = request.user.customer.addresses.get(uuid=uuid)
        except Address.DoesNotExist:
            return Responder.error_response('Address not found', status_code=status.HTTP_404_NOT_FOUND)
        serializer = AddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Responder.success_response('Address updated successfully', serializer.data)
        return Responder.error_response('Invalid data', serializer.errors)

    def delete(self, request, uuid):
        try:
            address = request.user.customer.addresses.get(uuid=uuid)
        except Address.DoesNotExist:
            return Responder.error_response('Address not found', status_code=status.HTTP_404_NOT_FOUND)
        address.delete()
        return Responder.success_response(message='Address deleted successfully', status_code=status.HTTP_200_OK, data=[ ])

