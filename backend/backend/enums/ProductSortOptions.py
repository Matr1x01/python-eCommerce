from enum import Enum


class ProductSortOptions(Enum):
    NAME_ASC = "name"
    NAME_DESC = "-name"
    PRICE_ASC = "selling_price"
    PRICE_DESC = "-selling_price"
    DATE_ADDED_ASC = "created_at"
    DATE_ADDED_DESC = "-created_at"
