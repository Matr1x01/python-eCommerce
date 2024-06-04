from rest_framework.views import APIView
from .models import Cart, CartItem, Wishlist, WishlistItem
from backend.utils import Responder
from backend.utils.ParseError import parse_error
from .serializers import CartSerializer, CartItemSerializer, WishlistSerializer, WishlistItemSerializer
from backend.enums.status import Status
from rest_framework import status



class WishlistAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(
                customer=request.user.customer, status=Status.ACTIVE).first()
            if wishlist:
                serializer = WishlistSerializer(wishlist)
                return Responder.success_response('Wishlist fetched successfully', serializer.data)
            wishlist_data = {
                'customer': request.user.customer,
                'status': Status.ACTIVE,
            }

            try:
                wishlist = Wishlist.objects.create(wishlist_data)
                serializer = WishlistSerializer(wishlist)
                return Responder.success_response('Wishlist fetched successfully', serializer.data)
            except Exception as e:
                return Responder.error_response(message='Error fetching wishlist', errors=parse_error(e))

        return Responder.error(message='Unauthorized', status=status.HTTP_401_UNAUTHORIZED)
    
    def post(self, request):
        if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(
                customer=request.user.customer, status=Status.ACTIVE).first()
            if wishlist:
                serializer = WishlistSerializer(wishlist)
                return Responder.success_response('Wishlist fetched successfully', serializer.data)
            wishlist_data = {
                'customer': request.user.customer,
                'status': Status.ACTIVE
            }

            try:
                wishlist = Wishlist.objects.create(wishlist_data)
                serializer = WishlistSerializer(wishlist)
                return Responder.success_response('Wishlist fetched successfully', serializer.data)
            except Exception as e:
                return Responder.error_response(message='Error fetching wishlist', errors=parse_error(e))

        return Responder.error(message='Unauthorized', status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request):
        if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(
                customer=request.user.customer, status=Status.ACTIVE).first()
            if wishlist:
                wishlist.delete()
                return Responder.success_response('Wishlist deleted successfully')
            return Responder.error(message='Wishlist not found', status=status.HTTP_404_NOT_FOUND)
        return Responder.error(message='Unauthorized', status=status.HTTP_401_UNAUTHORIZED)
    
    def put(self, request):
        if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(
                customer=request.user.customer, status=Status.ACTIVE).first()
            if wishlist:
                wishlist.delete()
                return Responder.success_response('Wishlist deleted successfully')
            return Responder.error(message='Wishlist not found', status=status.HTTP_404_NOT_FOUND)
        return Responder.error


class CartAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            cart = Cart.objects.filter(
                customer=request.user.customer, status=Status.ACTIVE).first()
            if cart:
                serializer = CartSerializer(cart)
                return Responder.success_response('Cart fetched successfully', serializer.data)
            cart_data = {
                'customer': request.user.customer,
                'status': Status.ACTIVE,
                'total_price': 0.00,
                'subtotal_price': 0.00,
                'total_items': 0,
                'discount': 0.00,
                'tax': 0.00,
                'shipping': 0.00,
                'total': 0.00,
                'address': None
            }

            try:
                cart = Cart.objects.create(cart_data)
                serializer = CartSerializer(cart)
                return Responder.success_response('Cart fetched successfully', serializer.data)
            except Exception as e:
                return Responder.error_response(message='Error fetching cart', errors=parse_error(e))

        return Responder.error(message='Unauthorized', status=status.HTTP_401_UNAUTHORIZED)
    
    def post(self, request):
        if request.user.is_authenticated:
            cart = Cart.objects.filter(
                customer=request.user.customer, status=Status.ACTIVE).first()
            if cart:
                serializer = CartSerializer(cart)
                return Responder.success_response('Cart fetched successfully', serializer.data)
            cart_data = {
                'customer': request.user.customer,
                'status': Status.ACTIVE,
                'total_price': 0.00,
                'subtotal_price': 0.00,
                'total_items': 0,
                'discount': 0.00,
                'tax': 0.00,
                'shipping': 0.00,
                'total': 0.00,
                'address': None
            }

            try:
                cart = Cart.objects.create(cart_data)
                serializer = CartSerializer(cart)
                return Responder.success_response('Cart fetched successfully', serializer.data)
            except Exception as e:
                return Responder.error_response(message='Error fetching cart', errors=parse_error(e))

        return Responder.error(message='Unauthorized', status=status.HTTP_401_UNAUTHORIZED)
    
