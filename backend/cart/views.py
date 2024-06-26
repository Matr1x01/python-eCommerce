from rest_framework.views import APIView
from .models import Cart, Wishlist
from backend.utils.Responder import Responder
from backend.utils.ParseError import parse_error
from .serializers import CartSerializer, CartItemSerializer, WishlistSerializer, WishlistItemSerializer, \
    CartAddressSerializer
from backend.enums.status import Status
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from product.models import Product

from backend.utils.get_default_address import get_default_address

from address.models import Address


def get_wishlist(user, status=Status.ACTIVE.value):
    return Wishlist.objects.get_or_create(customer=user.customer, status=status)[0]


def get_cart(user, status=Status.ACTIVE.value):
    cart = Cart.objects.filter(customer=user.customer, status=status).first()
    if cart:
        return cart
    try:
        address = user.customer.addresses.first()
        if not address:
            address = Address.objects.create(
                customer=user.customer, **get_default_address()
            )

        return Cart.objects.create(customer=user.customer, address=address)
    except Exception as exc:
        return exc


class AuthenticatedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def handle_errors(self, exc, status_code=status.HTTP_400_BAD_REQUEST):
        return Responder.error_response(message='Error processing request', errors=parse_error(exc),
                                        status_code=status_code)


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

        product = Product.objects.filter(
            slug=request.data.get('product')).first()
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
                wishlist_item_serializer.create(
                    {'wishlist': wishlist, 'product': product})

            wishlist.refresh_from_db()
            return Responder.success_response('Product added to wishlist successfully',
                                              WishlistSerializer(wishlist).data)

        return Responder.error_response(message='Error creating wishlist', errors=parse_error(wishlist))

    def delete(self, request):
        wishlist = get_wishlist(request.user)
        if wishlist:
            product = Product.objects.filter(
                slug=request.data.get('product')).first()
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
        try:
            cart = get_cart(request.user)
            return Responder.success_response('Cart fetched successfully', CartSerializer(cart).data)
        except Exception as exc:
            return self.handle_errors(exc)

    def post(self, request):
        cart_item_serializer = CartItemSerializer(data=request.data)
        if not cart_item_serializer.is_valid():
            return Responder.error_response(message='Error adding product to cart',
                                            errors=cart_item_serializer.errors)
        product = cart_item_serializer.validated_data.get('product')
        quantity = request.data.get('quantity')

        try:
            cart = get_cart(request.user)
            cart_item, created = cart.items.get_or_create(
                product=product,
                defaults={'price': product.get_price()}
            )

            if not created:
                cart_item.quantity += quantity
                if cart_item.quantity <= 0:
                    cart_item.delete()
                else:
                    cart_item.save()
            else:
                if quantity > 0:
                    cart_item.quantity = quantity
                    cart_item.save()
                else:
                    cart_item.delete()
                    return Responder.error_response(
                        message='Quantity must be greater than 0',
                        status_code=status.HTTP_400_BAD_REQUEST
                    )

            cart_serializer = CartSerializer(cart)

            cart_serializer.update(cart, cart_serializer.calculate_cart_values(cart))
            cart.refresh_from_db()
            return Responder.success_response(
                'Product added to cart successfully',
                CartSerializer(cart).data
            )
        except Exception as exc:
            return self.handle_errors(exc)

    def delete(self, request):
        try:
            cart = get_cart(request.user)
            product_slug = request.data.get('product')
            product = Product.objects.filter(slug=product_slug).first()

            if not product:
                return Responder.error_response(
                    message='Valid Product is required',
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            cart_item = cart.items.filter(product=product).first()

            if cart_item:
                cart_item.delete()

                cart_serializer = CartSerializer(cart)

                cart_serializer.update(cart, cart_serializer.calculate_cart_values(cart))

                cart.refresh_from_db()
                return Responder.success_response(
                    'Product removed from cart successfully',
                    CartSerializer(cart).data
                )

            return Responder.error_response(
                message='Product does not exist in cart',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as exc:
            return self.handle_errors(exc)


class CartAddressAPIView(AuthenticatedAPIView):
    def post(self, request):
        serializer = CartAddressSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Responder.error_response(message='Error updating cart address',
                                            errors=serializer.errors)

        try:
            cart = get_cart(request.user)
            cart.address = serializer.validated_data.get('address')
            cart_serializer = CartSerializer(cart)

            cart_serializer.update(cart, cart_serializer.calculate_cart_values(cart))
            return Responder.success_response('Cart address updated successfully', CartSerializer(cart).data)
        except Exception as exc:
            return Responder.error_response(message='Error updating cart address', errors=parse_error(exc))
