import os
import sys
from django.core.management import execute_from_command_line


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    modules_to_migrate = [
        'order',
        'product',
        'users',
        'cart',
        'address',
        'coupons',
        'image_module',
    ]

    extra_args = []

    sys.argv = ['manage.py', 'makemigrations'] + modules_to_migrate + extra_args

    execute_from_command_line(sys.argv)

    execute_from_command_line(['manage.py', 'migrate'])


if __name__ == "__main__":
    main()
