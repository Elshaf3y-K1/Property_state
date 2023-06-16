from django_filters import FilterSet, AllValuesFilter
from django_filters import DateTimeFilter, NumberFilter
from .models import Unit


class RobotFilter(FilterSet):
   
    min_price = NumberFilter(field_name='price', lookup_expr='gte')
    max_price = NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Unit
        fields = (
            'title' ,
            'bedrooms' ,
            'bathrooms' ,
            'type_property', 
            'min_price',
            'max_price',

            )