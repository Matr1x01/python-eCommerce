from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from users.models import Customer
from product.models import Product, Category, Brand
from cart.models import Cart
from order.models import Order
from backend.enums.status import Status
from backend.enums.PaymentMethod import PaymentMethod
from backend.enums.DeliveryMethod import DeliveryMethod
from rest_framework.authtoken.models import Token
from address.models import Address


class OrderTestCase(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name="Test", phone="1234567890")
        self.token = Token.objects.create(user=self.customer.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.key)

        self.brand = Brand.objects.create(name='Test Brand', slug='test-brand')
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            name='Test Product', slug='test-product', selling_price=100, cost_price=50, brand=self.brand)
        self.product.category.add(self.category)

        self.address = Address.objects.create(
            address="Test Address", area="Test Area", city="Test City", state="Test State",
            country="Test Country", postal_code="123456", customer=self.customer)
        self.cart = Cart.objects.create(customer=self.customer, status=Status.ACTIVE.value, address=self.address)
        self.cart.items.create(product=self.product, quantity=2, price=100)

        self.order_url = reverse('order')

    def test_create_order_valid_cart(self):
        data = {
            'payment_method': PaymentMethod.CASH_ON_DELIVERY.value,
            'delivery_method': DeliveryMethod.HOME_DELIVERY.value,
        }
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Order created successfully')
        self.assertTrue(Order.objects.filter(customer=self.customer).exists())

    def test_create_order_empty_cart(self):
        self.cart.items.all().delete()
        data = {
            'payment_method': PaymentMethod.CASH_ON_DELIVERY.value,
            'delivery_method': DeliveryMethod.HOME_DELIVERY.value,
        }
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_invalid_delivery_method(self):
        data = {
            'payment_method': PaymentMethod.CASH_ON_DELIVERY.value,
            'delivery_method': 'INVALID_METHOD',
        }
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_invalid_payment_method(self):
        data = {
            'payment_method': 'INVALID_METHOD',
            'delivery_method': DeliveryMethod.HOME_DELIVERY.value,
        }
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_no_active_cart(self):
        self.cart.status = Status.INACTIVE.value
        self.cart.save()
        data = {
            'payment_method': PaymentMethod.CASH_ON_DELIVERY.value,
            'delivery_method': DeliveryMethod.HOME_DELIVERY.value,
        }
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
