import django_filters
from .models import *
from django_filters import DateFilter


class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_created', lookup_expr='gte')
    end_date = DateFilter(field_name='date_created', lookup_expr='lte')

    class Meta:  # need minumum attributes
         model = Order
         fields = '__all__'  # all inputs
         exclude = ['customer', 'date_created']  # exclude these inputs from all inputs
