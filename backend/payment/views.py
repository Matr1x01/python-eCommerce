from rest_framework.views import APIView
from backend.enums.status import Status
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from backend.utils.ParseError import parse_error
from backend.utils.Responder import Responder

from .serializers import PaymentSerializer


class AuthenticatedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def handle_errors(self, exc, status_code=status.HTTP_400_BAD_REQUEST):
        return Responder.error_response(message='Error processing request', errors=parse_error(exc),
                                        status_code=status_code)


class PaymentAPIView(AuthenticatedAPIView):
    def get(self, request):
        customer = request.user.customer
        payments = customer.payments.all()
        serializer = PaymentSerializer(payments, many=True)
        return Responder.success_response('Payments fetched successfully', serializer.data)

    def post(self, request):
        order = request.user.customer.orders.filter(status=Status.ACTIVE.value).first()
        if not order:
            return Responder.error_response(message='User has no active order', status_code=status.HTTP_400_BAD_REQUEST)
        request.data['order'] = order.id
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.create({'order': order})
            return Responder.success_response('Payment created successfully', PaymentSerializer(payment).data)

        return Responder.error_response(message='Error creating payment', errors=serializer.errors)