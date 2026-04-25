from django_filters import rest_framework as filters
from .models import order
from django_filters.rest_framework import DjangoFilterBackend

class OrderFilter(filters.FilterSet):
    start_date = filters.DateTimeFilter(field_name="creation_date", lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name="creation_date", lookup_expr='lte')


    class Meta:
        model = order
        fields = ['start_date', 'end_date']