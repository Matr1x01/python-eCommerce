from rest_framework.views import APIView
from .models import Cart, CartItem, Wishlist, WishlistItem
from backend.utils.Responder import Responder
from backend.utils.ParseError import parse_error
from .serializers import CartSerializer, CartItemSerializer, WishlistSerializer, GetWishlistItemSerializer, \
    StoreWishlistItemSerializer
from backend.enums.status import Status
from rest_framework import status

from product.models import Product


def get_wishlist(user, status=Status.ACTIVE.value):
    wishlist = Wishlist.objects.filter(
        customer=user.customer, status=status).first()
    if wishlist:
        return wishlist
    wishlist_data = {
        'customer': user.customer,
        'status': status,
    }

    try:
        wishlist = Wishlist.objects.create(**wishlist_data)
        return wishlist
    except Exception as e:
        return e


class WishlistAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            wishlist = get_wishlist(request.user)
            if isinstance(wishlist, Wishlist):
                return Responder.success_response('Wishlist fetched successfully', WishlistSerializer(wishlist).data)
            return Responder.error(message='Error fetching wishlist', errors=parse_error(wishlist))

        return Responder.error_response(message='Unauthorized', status_code=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        if request.user.is_authenticated:
            product = Product.objects.filter(slug=request.data.get('product')).first()
            if not product:
                return Responder.error_response(message='Valid Product is required', status_code=status.HTTP_400_BAD_REQUEST)

            wishlist = get_wishlist(request.user)
            if isinstance(wishlist, Wishlist):
                if WishlistItem.objects.filter(wishlist=wishlist, product=product).exists():
                    return Responder.success_response('Wishlist fetched successfully', WishlistSerializer(wishlist).data)

                wishlist_item_data = {
                    'wishlist': wishlist.id,
                    'product': product.id,
                }
                wishlist_item_serializer = StoreWishlistItemSerializer(data=wishlist_item_data)
                if wishlist_item_serializer.is_valid():
                    wishlist_item_serializer.save()
                else:
                    return Responder.error_response(message='Error adding product to wishlist', errors=wishlist_item_serializer.errors)

                wishlist = Wishlist.objects.filter(id=wishlist.id).first()
                return Responder.success_response('Wishlist fetched successfully', WishlistSerializer(wishlist).data)

            return Responder.error_response(message='Error fetching wishlist', errors=parse_error(wishlist))

        return Responder.error_response(message='Unauthorized', status_code=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(
                customer=request.user.customer, status=Status.ACTIVE.value).first()
            if wishlist:
                wishlist.delete()
                return Responder.success_response('Wishlist deleted successfully')
            return Responder.error(message='Wishlist not found', status=status.HTTP_404_NOT_FOUND)
        return Responder.error(message='Unauthorized', status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(
                customer=request.user.customer, status=Status.ACTIVE.value).first()
            if wishlist:
                wishlist.delete()
                return Responder.success_response('Wishlist deleted successfully')
            return Responder.error(message='Wishlist not found', status=status.HTTP_404_NOT_FOUND)
        return Responder.error


class CartAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            cart = Cart.objects.filter(
                customer=request.user.customer, status=Status.ACTIVE.value).first()
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
                customer=request.user.customer, status=Status.ACTIVE.value).first()
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
