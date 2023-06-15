from django_filters import FilterSet, AllValuesFilter
from django_filters import DateTimeFilter, NumberFilter
from .models import Unit


class RobotFilter(FilterSet):
    # from_manufacturing_date = DateTimeFilter(field_name='manufacturing_date',
    #                                          lookup_expr='gte')
    # to_manufacturing_date = DateTimeFilter(field_name='manufacturing_date',
    #                                        lookup_expr='lte')
    min_price = NumberFilter(field_name='price', lookup_expr='gte')
    max_price = NumberFilter(field_name='price', lookup_expr='lte')
    # robotcategory_name = AllValuesFilter(field_name='robot_category__name')
    # manufacturer_name = AllValuesFilter(field_name='manufacturer__name')
 
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