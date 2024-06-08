from enum import Enum


class PaymentStatus(Enum):
    UNPAID = 1
    PAID = 2
    REFUNDED = 3
    PARTIALLY_REFUNDED = 4
    PAYMENT_FAILED = 5
    CANCELLED = 6
