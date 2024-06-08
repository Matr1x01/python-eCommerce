from enum import Enum


class OrderStatus(Enum):
    PENDING = 1
    CONFIRMED = 2
    CANCELLED = 3
    DELIVERED = 4
