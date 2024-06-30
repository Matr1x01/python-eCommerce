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
    modules_to_test = [
        'order.tests',
        'product.tests',
        'users.tests',
        'cart.tests',
        'address.tests',
        'coupons.tests'
    ]

    extra_args = ['--verbosity', '2']

    # Set the default settings module for the 'test' command.
    sys.argv = ['manage.py', 'test'] + modules_to_test + extra_args

    # Execute the command line utility with the arguments provided.
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
