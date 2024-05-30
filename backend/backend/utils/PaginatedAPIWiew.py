from django.core.paginator import Paginator, EmptyPage
from rest_framework.views import APIView
from backend.utils.PaginationData import pagination_data


class PaginatedAPIView(APIView):
    def get_paginated_response(self, queryset, serializer_class):
        per_page = self.request.GET.get('per_page', 10)
        current_page = self.request.GET.get('page', 1)
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