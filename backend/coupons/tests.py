from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import Customer
from product.models import Product, Category, Brand
from rest_framework.authtoken.models import Token

from coupons.models import Coupon


class CouponTestCase(TestCase):
    def setUp(self):
        self.brand1 = Brand.objects.create(
            name='Test Brand', slug="test-brand", description="This is a test brand")
        self.brand2 = Brand.objects.create(
            name='Test Brand 2', slug="test-brand-2")
        self.category1 = Category.objects.create(
            name='Test Category', slug="test-category", description="This is a test category")
        self.category2 = Category.objects.create(
            name='Test Category 2', slug="test-category-2")

        self.product1 = Product.objects.create(
            name='Test Product', slug="test-product", selling_price=100, cost_price=50, brand=self.brand1,
            discount_price=80)
        self.product2 = Product.objects.create(
            name='Test Product 2', slug="test-product-2", selling_price=200, cost_price=100, brand=self.brand2)
        self.product3 = Product.objects.create(
            name='Test Product 3', slug="test-product-3", selling_price=300, cost_price=150, brand=self.brand1,
            discount_price=250)

        self.product1.category.add(self.category1)
        self.product2.category.add(self.category2)
        self.product3.category.add(self.category1)

        self.customer = Customer.objects.create(name="Test", phone="1234567890")
        self.token = Token.objects.create(user=self.customer.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.key)

        self.coupon = Coupon.objects.create(code="TESTCOUPON", discount=20)

        self.coupon_url = reverse('apply-coupon')

    def test_coupon_apply_unauthenticated(self):
        self.client.credentials()
        response = self.client.post(self.coupon_url, data={"code": "TESTCOUPON"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_coupon_apply_invalid_coupon(self):
        response = self.client.post(self.coupon_url, data={"code": "INVALIDCOUPON"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_coupon_apply_without_cart(self):
        response = self.client.post(self.coupon_url, data={"code": "TESTCOUPON"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_coupon_apply(self):
        response = self.client.post(reverse('cart'), {'product': self.product2.slug, 'quantity': 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(self.coupon_url, data={"code": "TESTCOUPON"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        cart_response = self.client.get(reverse('cart')).data
        self.assertEqual(float(cart_response.get('data').get('total')), 190)
        self.assertEqual(float(cart_response.get('data').get('discount')), 20)

        response = self.client.post(reverse('cart'), {'product': self.product1.slug, 'quantity': 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        cart_response = self.client.get(reverse('cart')).data

        self.assertEqual(float(cart_response.get('data').get('total')), 270)
        self.assertEqual(float(cart_response.get('data').get('discount')), 20)

    def test_empty_cart_coupon_remove(self):
        response = self.client.post(reverse('cart'), {'product': self.product2.slug, 'quantity': 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(reverse('cart'), {'product': self.product1.slug, 'quantity': 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(self.coupon_url, data={"code": "TESTCOUPON"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(reverse('cart'), {'product': self.product1.slug}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse('cart')).data

        self.assertEqual(float(response.get('data').get('total')), 190)
        self.assertEqual(float(response.get('data').get('discount')), 20)

        response = self.client.post(reverse('cart'), {'product': self.product2.slug, 'quantity': -1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse('cart'))

        self.assertEqual(float(response.data.get('data').get('total')), 0)
        self.assertEqual(float(response.data.get('data').get('discount')), 0)

    def test_double_coupon_apply(self):
        response = self.client.post(reverse('cart'), {'product': self.product2.slug, 'quantity': 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(self.coupon_url, data={"code": "TESTCOUPON"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(self.coupon_url, data={"code": "TESTCOUPON"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
