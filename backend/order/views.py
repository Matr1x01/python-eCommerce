from rest_framework.views import APIView
from backend.enums.status import Status
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from backend.utils.ParseError import parse_error
from backend.utils.Responder import Responder
from order.serializers import OrderDetailsSerializer, OrderSerializer


class AuthenticatedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def handle_errors(self, exc, status_code=status.HTTP_400_BAD_REQUEST):
        return Responder.error_response(message='Error processing request', errors=parse_error(exc), status_code=status_code)


class OrderDetailsAPIView(AuthenticatedAPIView):
    def get(self, request, key):
        customer = request.user.customer
        order = customer.orders.filter(key=key).first()
        if not order:
            return Responder.error_response(message='Order not found', status_code=status.HTTP_404_NOT_FOUND)
        serializer = OrderDetailsSerializer(order)
        return Responder.success_response('Order fetched successfully', serializer.data)


class OrderAPIView(AuthenticatedAPIView):
    def get(self, request):
        customer = request.user.customer
        orders = customer.orders.all()
        serializer = OrderSerializer(orders, many=True)
        return Responder.success_response('Orders fetched successfully', serializer.data)

    def post(self, request):
        cart = request.user.customer.cart.filter(
            status=Status.ACTIVE.value).first()
        if not cart:
            return Responder.error_response(message='User has no active cart', status_code=status.HTTP_400_BAD_REQUEST)
        request.data['cart'] = cart.id
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.create({'cart': cart})
            return Responder.success_response('Order created successfully', OrderDetailsSerializer(order).data)

        return Responder.error_response(message='Error creating order', errors=serializer.errors)
