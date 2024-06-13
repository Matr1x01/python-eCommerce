from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import Customer, CustomUser


class UserTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='01765393016', password='12345678')
        self.customer = Customer.objects.create(
            name='test', phone='01765393016', user=self.user)

    def test_customer_login(self):
        url = reverse('login')
        data = {'phone': '01765393016', 'password': '12345678'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.data.get('data')
        self.assertIn('token', response_data)
        self.assertIn('customer', response_data)
        self.assertEqual(response_data['customer']['name'], 'test')
        self.assertEqual(response_data['customer']['phone'], '01765393016')
        customer_keys = ['name', 'phone', 'date_of_birth', 'gender']
        self.assertEqual(set(customer_keys), set(
            response_data['customer'].keys()))

    def test_customer_login_invalid_credentials(self):
        url = reverse('login')
        data = {'phone': '01765393016', 'password': '123456789'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_customer_login_invalid_phone(self):
        url = reverse('login')
        data = {'phone': '0176539301', 'password': '12345678'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_customer_register(self):
        url = reverse('register')
        data = {
            "phone": "01765393017",
            "password": "12345678",
            "name": "Mozharul Haq",
            "confirm_password": "12345678"
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.data.get('data')
        self.assertIn('token', response_data)
        self.assertIn('customer', response_data)
        self.assertEqual(response_data['customer']['name'], 'Mozharul Haq')
        self.assertEqual(response_data['customer']['phone'], '01765393017')
        customer_keys = ['name', 'phone', 'date_of_birth', 'gender']
        self.assertEqual(set(customer_keys), set(
            response_data['customer'].keys()))

    def test_customer_register_duplicate_phone(self):
        url = reverse('register')
        data = {
            "phone": "01765393016",
            "password": "12345678",
            "name": "Mozharul Haq",
            "confirm_password": "12345678"
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_customer_register_password_mismatch(self):
        url = reverse('register')
        data = {
            "phone": "01765393017",
            "password": "12345678",
            "name": "Mozharul Haq",
            "confirm_password": "123456789"
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_customer_detail(self):
        url = reverse('customer-detail')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.data.get('data')
        self.assertEqual(response_data['name'], 'test')
        self.assertEqual(response_data['phone'], '01765393016')
        customer_keys = ['name', 'phone', 'date_of_birth', 'gender']
        self.assertEqual(set(customer_keys), set(response_data.keys()))
    
    def test_customer_update(self):
        url = reverse('customer-update')
        self.client.force_authenticate(user=self.user)
        data = {
            "name": "Mozharul Haq",
            "date_of_birth": "1996-06-05",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.data.get('data')
        self.assertEqual(response_data['name'], 'Mozharul Haq')
        self.assertEqual(response_data['date_of_birth'], '1996-06-05')
        self.assertEqual(response_data['phone'], '01765393016')
        customer_keys = ['name', 'phone', 'date_of_birth', 'gender']
        self.assertEqual(set(customer_keys), set(response_data.keys()))

