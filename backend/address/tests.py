from django.test import TestCase

from .models import Address


#address = models.TextField()
# uuid = models.UUIDField(unique=True, editable=False, null=False, blank=False, default=uuid.uuid4)
# area = models.CharField(max_length=255)
# city = models.CharField(max_length=255)
# state = models.CharField(max_length=255, null=True, blank=True)
# country = models.CharField(max_length=255)
# postal_code = models.CharField(max_length=255)
class AddressTestCase(TestCase):
    def setUp(self):
        Address.objects.create(address="Test Address", area="Test Area", city="Test City", state="Test State",
                               country="Test Country", postal_code="123456")

    def test_address(self):
        address = Address.objects.get(address="Test Address")
        self.assertEqual(address.area, "Test Area")
        self.assertEqual(address.city, "Test City")
        self.assertEqual(address.state, "Test State")
        self.assertEqual(address.country, "Test Country")
        self.assertEqual(address.postal_code, "123456")

