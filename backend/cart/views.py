from rest_framework.views import APIView
from .models import Cart, CartItem, Wishlist, WishlistItem
from backend.utils.Responder import Responder
from backend.utils.ParseError import parse_error
from .serializers import CartSerializer, CartItemSerializer, WishlistSerializer, WishlistItemSerializer
from backend.enums.status import Status
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from product.models import Product


def get_wishlist(user, status=Status.ACTIVE.value):
    return Wishlist.objects.get_or_create(customer=user.customer, status=status)[0]


def get_cart(user, status=Status.ACTIVE.value):
    return Cart.objects.get_or_create(customer=user.customer, status=status)[0]


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
        wishlist_item_serializer = WishlistItemSerializer(data=request.data)
        if not wishlist_item_serializer.is_valid():
            return Responder.error_response(message='Error adding product to wishlist',
                                            errors=wishlist_item_serializer.errors)

        product = Product.objects.filter(slug=request.data.get('product')).first()
        if not product:
            return Responder.error_response(message='Valid Product is required',
                                            status_code=status.HTTP_400_BAD_REQUEST)

        wishlist = get_wishlist(request.user)
        if wishlist:
            wishlist_item = wishlist.items.filter(product=product).first()
            if wishlist_item:
                if wishlist_item.status == Status.ACTIVE.value:
                    return Responder.error_response(message='Product already exists in wishlist',
                                                    status_code=status.HTTP_400_BAD_REQUEST)
                wishlist_item.status = Status.ACTIVE.value
                wishlist_item.save()
            else:
                wishlist_item_serializer.create({'wishlist': wishlist, 'product': product})

            wishlist.refresh_from_db()
            return Responder.success_response('Product added to wishlist successfully',
                                              WishlistSerializer(wishlist).data)

        return Responder.error_response(message='Error creating wishlist', errors=parse_error(wishlist))

    def delete(self, request):
        wishlist = get_wishlist(request.user)
        if wishlist:
            product = Product.objects.filter(slug=request.data.get('product')).first()
            if not product:
                return Responder.error_response(message='Valid Product is required',
                                                status_code=status.HTTP_400_BAD_REQUEST)

            wishlist_item = wishlist.items.filter(product=product).first()
            if wishlist_item:
                wishlist_item.status = Status.INACTIVE.value
                wishlist_item.save()
                wishlist.refresh_from_db()
                return Responder.success_response('Product removed from wishlist successfully',
                                                  WishlistSerializer(wishlist).data)
            return Responder.error_response(message='Product does not exist in wishlist',
                                            status_code=status.HTTP_400_BAD_REQUEST)


class CartAPIView(AuthenticatedAPIView):

    def get(self, request):
        cart = get_cart(request.user)
        if isinstance(cart, Cart):
            return Responder.success_response('Cart fetched successfully', CartSerializer(cart).data)
        return Responder.error_response(message='Error fetching cart', errors=parse_error(cart))

    def post(self, request):
        cart_item_serializer = CartItemSerializer(data=request.data)
        if not cart_item_serializer.is_valid():
            return Responder.error_response(message='Error adding product to cart',
                                            errors=cart_item_serializer.errors)
        product = cart_item_serializer.validated_data.get('product')
        cart = get_cart(request.user)
        if cart:
            cart_item = cart.items.filter(product=product).first()
            if cart_item:
                cart_item.quantity += request.data.get('quantity')
                if cart_item.quantity < 0:
                    cart_item.quantity = 0
                cart_item.save()
            else:
                data = cart_item_serializer.validated_data
                data['cart'] = cart
                cart_item_serializer.create(data)
                cart_serializer = CartSerializer(cart)
                cart_serializer.update(cart_serializer.validated_data)
            cart.refresh_from_db()
            return Responder.success_response('Product added to cart successfully',
                                              CartSerializer(cart).data)

        return Responder.error_response(message='Error creating cart', errors=parse_error(cart))

    def delete(self, request):
        cart = get_cart(request.user)
        if cart:
            product = Product.objects.filter(slug=request.data.get('product')).first()
            if not product:
                return Responder.error_response(message='Valid Product is required',
                                                status_code=status.HTTP_400_BAD_REQUEST)

            cart_item = cart.items.filter(product=product).first()
            if cart_item:
                cart_item.delete()
                cart.refresh_from_db()
                return Responder.success_response('Product removed from cart successfully',
                                                  CartSerializer(cart).data)
            return Responder.error_response(message='Product does not exist in cart',
                                            status_code=status.HTTP_400_BAD_REQUEST)
        return Responder.error_response(message='Error fetching cart', errors=parse_error(cart))
