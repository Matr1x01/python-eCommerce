from django.core.paginator import Paginator


def pagination_data(paginator: Paginator, current_page: int):
    return {
        'per_page': paginator.per_page,
        'current_page': int(current_page),
        'item_count': paginator.count,
        'total_pages': paginator.num_pages
    }
