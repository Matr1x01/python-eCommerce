from django.core.paginator import Paginator, EmptyPage
from rest_framework.views import APIView
from backend.utils.PaginationData import pagination_data
from backend.enums.ProductSortOptions import ProductSortOptions


class PaginatedAPIView(APIView):
    def get_paginated_response(self, queryset, serializer_class):
        try:
            per_page = max(int(self.request.GET.get('per_page', 10)), 1)
            current_page = max(int(self.request.GET.get('page', 1)), 1)
        except ValueError:
            per_page, current_page = 10, 1

        sort_by = ProductSortOptions.NAME_ASC.value
        sort_by_param = self.request.GET.get('sort_by')
        if sort_by_param and hasattr(ProductSortOptions, sort_by_param):
            sort_by = getattr(ProductSortOptions, sort_by_param).value

        queryset = queryset.order_by(sort_by)

        paginator = Paginator(queryset, per_page)

        try:
            page = paginator.page(current_page)
        except EmptyPage:
            return {
                'items': [],
                'meta': {
                    'total_items': 0,
                    'total_pages': 0,
                    'current_page': current_page
                }
            }

        serializer = serializer_class(page, many=True)
        return {
            'items': serializer.data,
            'meta': pagination_data(paginator, current_page)
        }