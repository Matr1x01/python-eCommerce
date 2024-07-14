from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Product, Category, Brand


class ProductTests(APITestCase):

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

    def test_get_products(self):
        url = reverse('products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        products_list = response.data.get('data').get('items')
        self.assertEqual(len(products_list), 3)

        expected_products = [
            {'name': 'Test Product', 'slug': 'test-product', 'selling_price': 100, 'brand': {'name': 'Test Brand',
                                                                                             'slug': 'test-brand',
                                                                                             'logo': ''},
             'category': [{'name': 'Test Category', 'slug': "test-category"}], 'image': "", 'has_discount': True,
             'discount_price': 80.0},
            {'name': 'Test Product 2', 'slug': 'test-product-2', 'selling_price': 200, 'brand': {'name': 'Test Brand 2',
                                                                                                 'slug': 'test-brand-2',
                                                                                                 'logo': ''},
             'category': [{'name': 'Test Category 2', 'slug': "test-category-2"}], 'image': "", 'has_discount': False,
             'discount_price': 0},
            {'name': 'Test Product 3', 'slug': 'test-product-3', 'selling_price': 300, 'brand': {'name': 'Test Brand',
                                                                                                 'slug': 'test-brand',
                                                                                                 'logo': ''},
             'category': [{'name': 'Test Category', 'slug': "test-category"}], 'image': "", 'has_discount': True,
             'discount_price': 250.0}
        ]

        for product, expected in zip(products_list, expected_products):
            self.assertDictEqual(product, expected)

    def test_get_product_detail(self):
        url = reverse('product-detail', args=[self.product1.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        product_data = response.data.get('data').get('product')
        expected_product = {
            'name': 'Test Product',
            'slug': 'test-product',
            'selling_price': 100,
            'brand': {'name': 'Test Brand', 'slug': 'test-brand', 'logo': ''},
            'category': [{'name': 'Test Category', 'slug': "test-category"}],
            'images': [],
            'description': '',
            'has_discount': True,
            'discount_price': 80.0
        }
        self.assertDictEqual(product_data, expected_product)

    def test_get_brands(self):
        url = reverse('brands')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        brands_list = response.data.get('data').get('items')
        self.assertEqual(len(brands_list), 2)

        expected_brands = [
            {'name': 'Test Brand', 'slug': 'test-brand', 'logo': ''},
            {'name': 'Test Brand 2', 'slug': 'test-brand-2', 'logo': ''}
        ]

        for brand, expected in zip(brands_list, expected_brands):
            self.assertDictEqual(brand, expected)

    def test_get_brand_details(self):
        url = reverse('brand-detail', args=[self.brand1.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        brand_data = response.data.get('data').get('brand')
        expected_brand = {
            'name': 'Test Brand',
            'slug': 'test-brand',
            'description': 'This is a test brand',
            'logo': ''
        }
        self.assertDictEqual(brand_data, expected_brand)

        brand_products = response.data.get('data').get('products')
        self.assertEqual(len(brand_products), 2)

        expected_products = [
            {'name': 'Test Product', 'slug': 'test-product', 'selling_price': 100, 'brand': {'name': 'Test Brand',
                                                                                             'slug': 'test-brand',
                                                                                             'logo': ''},
             'category': [{'name': 'Test Category', 'slug': 'test-category'}], 'image': "", 'has_discount': True,
             'discount_price': 80.0},
            {'name': 'Test Product 3', 'slug': 'test-product-3', 'selling_price': 300, 'brand': {'name': 'Test Brand',
                                                                                                 'slug': 'test-brand',
                                                                                                 'logo': ''},
             'category': [{'name': 'Test Category', 'slug': 'test-category'}], 'image': "", 'has_discount': True,
             'discount_price': 250.0}
        ]

        for product, expected in zip(brand_products, expected_products):
            self.assertDictEqual(product, expected)

    def test_get_categories(self):
        url = reverse('category')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        categories_list = response.data.get('data').get('items')
        self.assertEqual(len(categories_list), 2)

        expected_categories = [
            {'name': 'Test Category', 'slug': 'test-category'},
            {'name': 'Test Category 2', 'slug': 'test-category-2'}
        ]

        for category, expected in zip(categories_list, expected_categories):
            self.assertDictEqual(category, expected)

    def test_get_category_details(self):
        url = reverse('category-detail', args=[self.category1.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        category_data = response.data.get('data').get('category')
        expected_category = {
            'name': 'Test Category',
            'slug': 'test-category',
            'description': 'This is a test category'
        }
        self.assertDictEqual(category_data, expected_category)

        category_products = response.data.get('data').get('products')
        self.assertEqual(len(category_products), 2)

        expected_products = [
            {'name': 'Test Product', 'slug': 'test-product', 'selling_price': 100, 'brand': {'name': 'Test Brand',
                                                                                             'slug': 'test-brand',
                                                                                             'logo': ''},
             'category': [{'name': 'Test Category', 'slug': 'test-category'}], 'image': "", 'has_discount': True,
             'discount_price': 80.0},
            {'name': 'Test Product 3', 'slug': 'test-product-3', 'selling_price': 300, 'brand': {'name': 'Test Brand',
                                                                                                 'slug': 'test-brand',
                                                                                                 'logo': ''},
             'category': [{'name': 'Test Category', 'slug': 'test-category'}], 'image': "", 'has_discount': True,
             'discount_price': 250.0}
        ]

        for product, expected in zip(category_products, expected_products):
            self.assertDictEqual(product, expected)

    def test_get_non_existent_product(self):
        url = reverse('product-detail', kwargs={'slug': 'test-product-4'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_non_existent_brand(self):
        url = reverse('brand-detail', kwargs={'slug': 'test-brand-3'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_non_existent_category(self):
        url = reverse('category-detail', kwargs={'slug': 'test-category-3'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_pagination(self):
        url = reverse('products') + '?per_page=2'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('data').get('items')), 2)
        self.assertEqual(response.data.get('data').get('meta').get('per_page'), 2)

    def test_get_product_search(self):
        url = reverse('product-search') + '?query=Product%202'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        products_list = response.data.get('data')
        self.assertEqual(len(products_list), 1)

        expected_products = [
            {'name': 'Test Product 2', 'slug': 'test-product-2'},
        ]

        for product, expected in zip(products_list, expected_products):
            self.assertDictEqual(product, expected)
