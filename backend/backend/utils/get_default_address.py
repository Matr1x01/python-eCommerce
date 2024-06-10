import os


def get_default_address():
    address = os.getenv('DEFAULT_ADDRESS')
    postal_code = os.getenv('DEFAULT_POST_CODE')
    city = os.getenv('DEFAULT_CITY')
    country = os.getenv('DEFAULT_COUNTRY')
    return {
        'address': address,
        'postal_code': postal_code,
        'city': city,
        'country': country
    }
