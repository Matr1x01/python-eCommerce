from rest_framework.views import APIView
from .models import Cart, CartItem, Wishlist, WishlistItem
from backend.utils.Responder import Responder
from backend.utils.ParseError import parse_error
from .serializers import CartSerializer, CartItemSerializer, WishlistSerializer, GetWishlistItemSerializer, \
    WishlistItemSerializer
from backend.enums.status import Status
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from product.models import Product


def get_wishlist(user, status=Status.ACTIVE.value):
    return Wishlist.objects.filter(customer=user.customer, status=status).first()

def get_cart(user, status=Status.ACTIVE.value):
    return Cart.objects.filter(customer=user.customer, status=status).first()

class AuthenticatedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def handle_errors(self, exc, status=status.HTTP_400_BAD_REQUEST):
        return Responder.error_response(message='Error processing request', errors=parse_error(exc), status_code=status)


class WishlistAPIView(AuthenticatedAPIView):
    def get(self, request):
        wishlist = get_wishlist(request.user)
        if isinstance(wishlist, Wishlist):
            return Responder.success_response('Wishlist fetched successfully', WishlistSerializer(wishlist).data)
        return Responder.error(message='Error fetching wishlist', errors=parse_error(wishlist))

    def post(self, request):
        if request.user.is_authenticated:
            wishlist_item_serializer = WishlistItemSerializer(
                data=request.data)
            if wishlist_item_serializer.is_valid():
                product = Product.objects.filter(
                    slug=request.data.get('product')).first()
                if not product:
                    return Responder.error_response(message='Valid Product is required', status_code=status.HTTP_400_BAD_REQUEST)
            else:
                return Responder.error_response(message='Error adding product to wishlist', errors=wishlist_item_serializer.errors)

            wishlist = get_wishlist(request.user)

            if isinstance(wishlist, Wishlist):
                exists_in_wishlist = WishlistItem.objects.filter(
                    wishlist=wishlist, product=product).first()
                if exists_in_wishlist:
                    if exists_in_wishlist.status == Status.INACTIVE.value:
                        exists_in_wishlist.status = Status.ACTIVE.value
                        exists_in_wishlist.save()

                        wishlist.refresh_from_db()

                    return Responder.success_response('Wishlist fetched successfully', WishlistSerializer(wishlist).data)

                wishlist_item_data = {
                    'wishlist': wishlist,
                    'product': product,
                }
                print(wishlist_item_data)

                try:
                    WishlistItem.objects.create(**wishlist_item_data)
                except Exception as e:
                    return Responder.error_response(message='Error adding product to wishlist', errors=parse_error(e))

                wishlist.refresh_from_db()

                return Responder.success_response('Wishlist fetched successfully', WishlistSerializer(wishlist).data)

            return Responder.error_response(message='Error fetching wishlist', errors=parse_error(wishlist))

        return Responder.error_response(message='Unauthorized', status_code=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        if request.user.is_authenticated:
            wishlist_item_serializer = WishlistItemSerializer(
                data=request.data)
            if wishlist_item_serializer.is_valid():
                product = Product.objects.filter(
                    slug=request.data.get('product')).first()
                if not product:
                    return Responder.error_response(message='Valid Product is required', status_code=status.HTTP_400_BAD_REQUEST)

                wishlist = get_wishlist(request.user)
                if isinstance(wishlist, Wishlist):
                    exists_in_wishlist = WishlistItem.objects.filter(
                        wishlist=wishlist, product=product, status=Status.ACTIVE.value).first()
                    if exists_in_wishlist:
                        exists_in_wishlist.status = Status.INACTIVE.value
                        exists_in_wishlist.save()

                        wishlist.refresh_from_db()

                        return Responder.success_response('Wishlist item deleted successfully', WishlistSerializer(wishlist).data)

                    return Responder.error_response(message='Product not found in wishlist', status_code=status.HTTP_404_NOT_FOUND)

                return Responder.error_response(message='Error deleting wishlist', errors=parse_error(wishlist))

        return Responder.error(message='Unauthorized', status=status.HTTP_401_UNAUTHORIZED)


class CartAPIView(AuthenticatedAPIView):

    def get(self, request):
        if request.user.is_authenticated:
            cart = get_cart(request.user)
            if isinstance(cart, Cart):
                return Responder.success_response('Cart fetched successfully', CartSerializer(cart).data)
            return Responder.error(message='Error fetching cart', errors=parse_error(cart))

        return Responder.error_response(message='Unauthorized', status_code=status.HTTP_401_UNAUTHORIZED)
    
    def post(self, request):
        pass