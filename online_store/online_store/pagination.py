from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.utils.functional import cached_property
import math


class PrecountedPaginator(Paginator):
    """Paginator whose total comes from a cheaper query supplied by the caller."""
    count_source = None

    @cached_property
    def count(self):
        return self.count_source.count() if self.count_source is not None else super().count

class CustomPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        total_pages = math.ceil(self.page.paginator.count / self.page_size)

        return Response({
            'count': self.page.paginator.count,
            'total_pages': total_pages,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })