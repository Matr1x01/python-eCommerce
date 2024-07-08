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

from backend.enums.OrderStatus import OrderStatus


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

        self.product1 = Product.objects.create(
            name='Test Product 1', slug='test-product-1', selling_price=150, cost_price=100, brand=self.brand)

        self.product.category.add(self.category)
        self.product1.category.add(self.category)

        self.address = Address.objects.create(
            address="Test Address", area="Test Area", city="Test City", state="Test State",
            country="Test Country", postal_code="123456", customer=self.customer)

        self.order_url = reverse('order')

    def test_create_order_valid_cart(self):
        cart_response = self.client.post(reverse('cart'), {'product': self.product.slug, 'quantity': 1}, format='json')
        self.assertEqual(cart_response.status_code, status.HTTP_200_OK)
        data = {
            'payment_method': PaymentMethod.CASH_ON_DELIVERY.value,
            'delivery_method': DeliveryMethod.HOME_DELIVERY.value,
        }
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Order created successfully')
        self.assertTrue(Order.objects.filter(customer=self.customer).exists())

    def test_create_order_empty_cart(self):
        Cart.objects.all().delete()
        data = {
            'payment_method': PaymentMethod.CASH_ON_DELIVERY.value,
            'delivery_method': DeliveryMethod.HOME_DELIVERY.value,
        }
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_no_cart_items(self):
        cart_response = self.client.get(reverse('cart'), format='json')
        self.assertEqual(cart_response.status_code, status.HTTP_200_OK)
        data = {
            'payment_method': PaymentMethod.CASH_ON_DELIVERY.value,
            'delivery_method': DeliveryMethod.HOME_DELIVERY.value,
        }
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_invalid_delivery_method(self):
        cart_response = self.client.post(reverse('cart'), {'product': self.product.slug, 'quantity': 1}, format='json')
        self.assertEqual(cart_response.status_code, status.HTTP_200_OK)
        data = {
            'payment_method': PaymentMethod.CASH_ON_DELIVERY.value,
            'delivery_method': 'INVALID_METHOD',
        }
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_invalid_payment_method(self):
        cart_response = self.client.post(reverse('cart'), {'product': self.product.slug, 'quantity': 1}, format='json')
        self.assertEqual(cart_response.status_code, status.HTTP_200_OK)
        data = {
            'payment_method': 'INVALID_METHOD',
            'delivery_method': DeliveryMethod.HOME_DELIVERY.value,
        }
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_orders(self):
        cart_response = self.client.post(reverse('cart'), {'product': self.product.slug, 'quantity': 1}, format='json')
        self.assertEqual(cart_response.status_code, status.HTTP_200_OK)

        data = {
            'payment_method': PaymentMethod.CASH_ON_DELIVERY.value,
            'delivery_method': DeliveryMethod.HOME_DELIVERY.value,
        }
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cart_response = self.client.post(reverse('cart'), {'product': self.product.slug, 'quantity': 1}, format='json')
        self.assertEqual(cart_response.status_code, status.HTTP_200_OK)
        cart_response = self.client.post(reverse('cart'), {'product': self.product1.slug, 'quantity': 1}, format='json')
        self.assertEqual(cart_response.status_code, status.HTTP_200_OK)
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('data')), 2)
        keys = ["key", "total", "total_items", "date", "order_status", "payment_status", "payment_method_name",
                "delivery_method_name"]

        for key in keys:
            self.assertTrue(key in response.data.get('data')[0])

        self.assertEqual(float(response.data.get('data')[0].get('total')), 110)
        self.assertEqual(response.data.get('data')[0].get('total_items'), 1)
        self.assertEqual(response.data.get('data')[0].get('payment_status'), 'UNPAID')
        self.assertEqual(response.data.get('data')[0].get('order_status'), 'PENDING')
        self.assertEqual(response.data.get('data')[0].get('payment_method_name'), 'CASH_ON_DELIVERY')
        self.assertEqual(response.data.get('data')[0].get('delivery_method_name'), 'HOME_DELIVERY')

        self.assertEqual(float(response.data.get('data')[1].get('total')), 260)
        self.assertEqual(response.data.get('data')[1].get('total_items'), 2)
        self.assertEqual(response.data.get('data')[1].get('payment_status'), 'UNPAID')
        self.assertEqual(response.data.get('data')[1].get('order_status'), 'PENDING')
        self.assertEqual(response.data.get('data')[1].get('payment_method_name'), 'CASH_ON_DELIVERY')
        self.assertEqual(response.data.get('data')[1].get('delivery_method_name'), 'HOME_DELIVERY')

    def test_get_order_details(self):
        cart_response = self.client.post(reverse('cart'), {'product': self.product.slug, 'quantity': 1}, format='json')
        self.assertEqual(cart_response.status_code, status.HTTP_200_OK)
        cart_response = self.client.post(reverse('cart'), {'product': self.product1.slug, 'quantity': 1}, format='json')
        self.assertEqual(cart_response.status_code, status.HTTP_200_OK)
        data = {
            'payment_method': PaymentMethod.CASH_ON_DELIVERY.value,
            'delivery_method': DeliveryMethod.HOME_DELIVERY.value,
        }
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse('order-detail', kwargs={'key': response.data.get('data')[0].get('key')}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        keys = ['key', 'total', 'tax', 'shipping', 'discount', 'sub_total', 'total_items', 'date', 'order_status',
                'payment_status', 'payment_method', 'delivery_method', 'ordered_items', "address"]

        for key in keys:
            self.assertTrue(key in response.data.get('data'))

        self.assertEqual(len(response.data.get('data').get('ordered_items')), 2)
        item_keys = ['quantity', 'price', 'total', 'product_name', 'product_slug', 'product_image']
        for key in item_keys:
            self.assertTrue(key in response.data.get('data').get('ordered_items')[0])

        self.assertEqual(float(response.data.get('data').get('total')), 260)
        self.assertEqual(float(response.data.get('data').get('tax')), 0)
        self.assertEqual(float(response.data.get('data').get('shipping')), 10)
        self.assertEqual(float(response.data.get('data').get('discount')), 0)
        self.assertEqual(float(response.data.get('data').get('sub_total')), 250)
        self.assertEqual(response.data.get('data').get('total_items'), 2)
        self.assertEqual(response.data.get('data').get('payment_status'), 'UNPAID')
        self.assertEqual(response.data.get('data').get('order_status'), 'PENDING')
        self.assertEqual(response.data.get('data').get('payment_method'), PaymentMethod.CASH_ON_DELIVERY.name)
        self.assertEqual(response.data.get('data').get('delivery_method'), DeliveryMethod.HOME_DELIVERY.name)

    def test_order_cancel(self):
        cart_response = self.client.post(reverse('cart'), {'product': self.product.slug, 'quantity': 1}, format='json')
        self.assertEqual(cart_response.status_code, status.HTTP_200_OK)
        data = {
            'payment_method': PaymentMethod.CASH_ON_DELIVERY.value,
            'delivery_method': DeliveryMethod.HOME_DELIVERY.value,
        }
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        key = response.data.get('data')[0].get('key')
        response = self.client.post(reverse('order-cancel', kwargs={'key': key}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('message'), 'Order cancelled successfully')
        self.assertEqual(Order.objects.filter(key=key).first().order_status, OrderStatus.CANCELLED.value)

    def test_order_cancel_confirmed_order(self):
        cart_response = self.client.post(reverse('cart'), {'product': self.product.slug, 'quantity': 1}, format='json')
        self.assertEqual(cart_response.status_code, status.HTTP_200_OK)
        data = {
            'payment_method': PaymentMethod.CASH_ON_DELIVERY.value,
            'delivery_method': DeliveryMethod.HOME_DELIVERY.value,
        }
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        key = response.data.get('data')[0].get('key')
        order = Order.objects.filter(key=key).first()
        order.order_status = OrderStatus.CONFIRMED.value
        order.save()
        response = self.client.post(reverse('order-cancel', kwargs={'key': key}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.filter(key=key).first().order_status, OrderStatus.CONFIRMED.value)
