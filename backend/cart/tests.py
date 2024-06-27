from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import Customer
from product.models import Product, Category, Brand
from rest_framework.authtoken.models import Token


class CartTestCase(TestCase):
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

        self.cart_url = reverse('cart')

    def test_get_cart_unauthorized(self):
        self.client.credentials()
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_cart_authorized(self):
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('data').get('subtotal_price'), "0.00")
        self.assertEqual(response.data.get('data').get('total_items'), 0)
        self.assertEqual(response.data.get('data').get('discount'), "0.00")
        self.assertEqual(response.data.get('data').get('tax'), "0.00")
        self.assertEqual(response.data.get('data').get('shipping'), "0.00")
        self.assertEqual(response.data.get('data').get('total'), "0.00")
        self.assertEqual(response.data.get('data').get('items'), [])

    def test_add_to_cart(self):
        response = self.client.post(self.cart_url, {'product': self.product1.slug, 'quantity': 2}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(self.cart_url, {'product': self.product2.slug, 'quantity': 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('data').get('total_items'), 3)
        self.assertEqual(response.data.get('data').get('subtotal_price'), "360.00")
        self.assertEqual(response.data.get('data').get('discount'), "0.00")
        self.assertEqual(response.data.get('data').get('tax'), "0.00")
        self.assertEqual(response.data.get('data').get('shipping'), "10.00")
        self.assertEqual(response.data.get('data').get('total'), "370.00")
        self.assertEqual(len(response.data.get('data').get('items')), 2)

    def test_reduce_quantity(self):
        response = self.client.post(self.cart_url, {'product': self.product1.slug, 'quantity': 2}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(self.cart_url, {'product': self.product1.slug, 'quantity': -1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('data').get('total_items'), 1)
        self.assertEqual(response.data.get('data').get('subtotal_price'), "80.00")
        self.assertEqual(response.data.get('data').get('discount'), "0.00")
        self.assertEqual(response.data.get('data').get('tax'), "0.00")
        self.assertEqual(response.data.get('data').get('shipping'), "10.00")
        self.assertEqual(response.data.get('data').get('total'), "90.00")
        self.assertEqual(len(response.data.get('data').get('items')), 1)

    def test_reduce_boundary_test(self):
        response = self.client.post(self.cart_url, {'product': self.product1.slug, 'quantity': 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(self.cart_url, {'product': self.product1.slug, 'quantity': -1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('data').get('total_items'), 0)
        self.assertEqual(response.data.get('data').get('subtotal_price'), "0.00")
        self.assertEqual(response.data.get('data').get('discount'), "0.00")
        self.assertEqual(response.data.get('data').get('tax'), "0.00")
        self.assertEqual(response.data.get('data').get('shipping'), "0.00")
        self.assertEqual(response.data.get('data').get('total'), "0.00")
        self.assertEqual(len(response.data.get('data').get('items')), 0)
        response = self.client.post(self.cart_url, {'product': self.product1.slug, 'quantity': -1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remove_from_cart(self):
        response = self.client.post(self.cart_url, {'product': self.product1.slug, 'quantity': 2}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(self.cart_url, {'product': self.product2.slug, 'quantity': 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.cart_url, {'product': self.product1.slug}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('data').get('total_items'), 1)
        self.assertEqual(response.data.get('data').get('subtotal_price'), "200.00")
        self.assertEqual(response.data.get('data').get('discount'), "0.00")
        self.assertEqual(response.data.get('data').get('tax'), "0.00")
        self.assertEqual(response.data.get('data').get('shipping'), "10.00")
        self.assertEqual(response.data.get('data').get('total'), "210.00")
        self.assertEqual(len(response.data.get('data').get('items')), 1)
        response = self.client.delete(self.cart_url, {'product': self.product2.slug}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('data').get('total_items'), 0)
        self.assertEqual(response.data.get('data').get('subtotal_price'), "0.00")
        self.assertEqual(response.data.get('data').get('discount'), "0.00")
        self.assertEqual(response.data.get('data').get('tax'), "0.00")
        self.assertEqual(response.data.get('data').get('shipping'), "0.00")
        self.assertEqual(response.data.get('data').get('total'), "0.00")
        self.assertEqual(len(response.data.get('data').get('items')), 0)

    def test_invalid_product_add(self):
        response = self.client.post(self.cart_url, {'product': 'invalid-product', 'quantity': 2}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_product_remove(self):
        response = self.client.delete(self.cart_url, {'product': 'invalid-product'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_negative_quantity(self):
        response = self.client.post(self.cart_url, {'product': self.product1.slug, 'quantity': -2}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class WishlistTestCase(TestCase):
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

        self.wishlist_url = reverse('wishlist')

    def test_get_wishlist_unauthorized(self):
        self.client.credentials()
        response = self.client.get(self.wishlist_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_wishlist_authorized(self):
        response = self.client.get(self.wishlist_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('data').get('items')), 0)

    def test_add_to_wishlist(self):
        response = self.client.post(self.wishlist_url, {'product': self.product1.slug}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(self.wishlist_url, {'product': self.product2.slug}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('data').get('items')), 2)

    def test_remove_from_wishlist(self):
        response = self.client.post(self.wishlist_url, {'product': self.product1.slug}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(self.wishlist_url, {'product': self.product2.slug}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.wishlist_url, {'product': self.product1.slug}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('data').get('items')), 1)
        response = self.client.delete(self.wishlist_url, {'product': self.product2.slug}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('data').get('items')), 0)

    def test_invalid_product_add(self):
        response = self.client.post(self.wishlist_url, {'product': 'invalid-product'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_product_remove(self):
        response = self.client.delete(self.wishlist_url, {'product': 'invalid-product'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_product_add(self):
        response = self.client.post(self.wishlist_url, {'product': self.product1.slug}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(self.wishlist_url, {'product': self.product1.slug}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.get(self.wishlist_url)
        self.assertEqual(len(response.data.get('data').get('items')), 1)

    def test_duplicate_product_remove(self):
        response = self.client.post(self.wishlist_url, {'product': self.product1.slug}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.wishlist_url, {'product': self.product1.slug}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.wishlist_url, {'product': self.product1.slug}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


