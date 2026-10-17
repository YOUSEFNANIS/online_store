from django_filters import rest_framework as filters
from .models import order, product
from django_filters.rest_framework import DjangoFilterBackend

class OrderFilter(filters.FilterSet):
    start_date = filters.DateTimeFilter(field_name="creation_date", lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name="creation_date", lookup_expr='lte')


    class Meta:
        model = order
        fields = ['start_date', 'end_date']


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    in_stock = filters.BooleanFilter(method='filter_in_stock')
    seller = filters.NumberFilter(field_name='seller_id')
    category = filters.NumberFilter(field_name='category_id')

    def filter_in_stock(self, queryset, name, value):
        return queryset.filter(inventory__gt=0) if value else queryset

    class Meta:
        model = product
        fields = ['min_price', 'max_price', 'in_stock', 'seller', 'category']
