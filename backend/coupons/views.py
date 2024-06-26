from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from backend.enums.status import Status
from rest_framework import status

from .models import Coupon
from .serializers import ApplyCouponSerializer
from backend.utils.Responder import Responder


class CouponApplyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ApplyCouponSerializer(data=request.data)

        if not serializer.is_valid():
            return Responder.error_response(message='Error applying coupon', errors=serializer.errors)

        customer = request.user.customer

        if not customer:
            return Responder.error_response(message='Customer not found', status_code=status.HTTP_404_NOT_FOUND)

        cart = customer.cart.filter(status=Status.ACTIVE.value).first()

        if not cart or cart.total_items == 0:
            return Responder.error_response(message='Cart not found', status_code=status.HTTP_404_NOT_FOUND)

        if cart.coupon:
            return Responder.error_response(message='Coupon already applied', status_code=status.HTTP_400_BAD_REQUEST)

        coupon = serializer.validated_data.get('code')
        coupon = Coupon.objects.filter(code=coupon).first()

        if not coupon:
            return Responder.error_response(message='Coupon not found', status_code=status.HTTP_404_NOT_FOUND)

        cart_total_price = cart.total - cart.discount

        if cart_total_price < 0:
            return Responder.error_response(message='Cart total price is less than 0', status_code=status.HTTP_400_BAD_REQUEST)

        cart.discount = coupon.discount
        cart.total = cart_total_price
        cart.coupon = coupon

        cart.save()

        return Responder.success_response('Coupon applied successfully', {'discount': coupon.discount})




