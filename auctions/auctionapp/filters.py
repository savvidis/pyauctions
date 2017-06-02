from .models import *
import django_filters
from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Div


cat = AssetPropertyType.objects.order_by().values_list('description') # returns a dictionary
areas = GeoAreas.objects.order_by().values_list('name') # returns a dictionary

CATEGORIES_MAJOR = [(x[0], x[0]) for x in cat]
areas = [(x[0], x[0]) for x in areas]
# print(CATEGORIES_MAJOR)

class AuctionFilter(django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
        super(AuctionFilter, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'control-label'
        self.helper.field_class = 'selectpicker'
        self.helper.layout = Layout(
            Div(
                'category_major', css_class="col-md-3",
            ),
            Div(
                'area', css_class="col-md-5",
            )
        )
    category_major = django_filters.ChoiceFilter(choices=CATEGORIES_MAJOR)

    # city = django_filters.CharFilter(lookup_expr='icontains')
    area = django_filters.ChoiceFilter(choices=areas)
    # area = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = AssetProperty
        fields = ['category_major', 'area', ]
