from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import Customer
from .models import Address
from rest_framework.authtoken.models import Token


class AddressTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name="Test", phone="1234567890")
        self.address = Address.objects.create(
            address="Test Address", area="Test Area", city="Test City", state="Test State",
            country="Test Country", postal_code="123456", customer=self.customer)
        self.token = Token.objects.create(user=self.customer.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.key)
        self.address_url = reverse('addresses')
        self.detail_url = reverse('address-detail', kwargs={'uuid': self.address.uuid})

    def test_get_addresses_unauthorized(self):
        self.client.credentials()  # Clear credentials
        response = self.client.get(self.address_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_addresses_authorized(self):
        response = self.client.get(self.address_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        address = response.data.get('data')[0]
        self.assertEqual(address['area'], "Test Area")
        self.assertEqual(address['city'], "Test City")
        self.assertEqual(address['state'], "Test State")
        self.assertEqual(address['country'], "Test Country")
        self.assertEqual(address['postal_code'], "123456")
        self.assertEqual(address['address'], "Test Address")

    def test_create_address_unauthorized(self):
        self.client.credentials()  # Clear credentials
        address_data = {
            "address": "Test Address 2",
            "area": "Test Area 2",
            "city": "Test City 2",
            "state": "Test State 2",
            "country": "Test Country 2",
            "postal_code": "654321"
        }
        response = self.client.post(self.address_url, address_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_address_authorized(self):
        address_data = {
            "address": "Test Address 2",
            "area": "Test Area 2",
            "city": "Test City 2",
            "state": "Test State 2",
            "country": "Test Country 2",
            "postal_code": "654321"
        }
        response = self.client.post(self.address_url, address_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        address = response.data.get('data')
        self.assertEqual(address['area'], "Test Area 2")
        self.assertEqual(address['city'], "Test City 2")
        self.assertEqual(address['state'], "Test State 2")
        self.assertEqual(address['country'], "Test Country 2")
        self.assertEqual(address['postal_code'], "654321")
        self.assertEqual(address['address'], "Test Address 2")

    def test_get_address_unauthorized(self):
        self.client.credentials()  # Clear credentials
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_address_authorized(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        address = response.data.get('data')
        self.assertEqual(address['area'], "Test Area")
        self.assertEqual(address['city'], "Test City")
        self.assertEqual(address['state'], "Test State")
        self.assertEqual(address['country'], "Test Country")
        self.assertEqual(address['postal_code'], "123456")
        self.assertEqual(address['address'], "Test Address")

    def test_update_address_unauthorized(self):
        self.client.credentials()  # Clear credentials
        address_data = {
            "address": "Test Address 3",
            "area": "Test Area 3",
            "city": "Test City 3",
            "state": "Test State 3",
            "country": "Test Country 3",
            "postal_code": "654321"
        }
        response = self.client.put(self.detail_url, address_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    #check for invalid uuid 404
    def test_update_address_invalid_uuid(self):
        response = self.client.put(reverse('address-detail', kwargs={'uuid': '12345678-1234-5678-1234-567812345678'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_address_authorized(self):
        address_data = {
            "address": "Test Address 3",
            "area": "Test Area 3",
            "city": "Test City 3",
            "state": "Test State 3",
            "country": "Test Country 3",
            "postal_code": "654321"
        }
        response = self.client.put(self.detail_url, address_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        address = response.data.get('data')
        self.assertEqual(address['area'], "Test Area 3")
        self.assertEqual(address['city'], "Test City 3")
        self.assertEqual(address['state'], "Test State 3")
        self.assertEqual(address['country'], "Test Country 3")
        self.assertEqual(address['postal_code'], "654321")
        self.assertEqual(address['address'], "Test Address 3")
