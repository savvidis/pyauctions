from .models import *
import django_filters
from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Div,Field
import datetime

from dal import autocomplete
import dal
from dal import widgets
import dal_select2

cat = AssetType.objects.order_by('description').values_list('description') # returns a dictionary

areas = GeoAreas.objects.order_by('name').values_list('name').distinct() # returns a dictionary
cities = GeoCities.objects.order_by('name').values_list('name')

CATEGORIES_MAJOR = [(x[0], x[0]) for x in cat]
areas = [(x[0], x[0]) for x in areas]
cities = [(x[0], x[0]) for x in cities]
dates_choices = [(1,'Active'),(0,'Passive')]

CATEGORIES_MINOR = []

cat_minor = AssetType.objects.order_by('synonyms').values_list('synonyms')
for y in cat_minor:
    for x in y:
        for w in x:
            CATEGORIES_MINOR.append((w, w))

# print(CATEGORIES_MAJOR)

class AuctionFilter(django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
        super(AuctionFilter, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'control-label'
        self.helper.field_class = 'selectpicker'
        self.helper.layout = Layout(
            Div(
                'asset_type', css_class="col-md-2",
            ),
            Div(
                'area', css_class="col-md-5",
            ),
            Div(
                'starting_price', css_class="col-md-2",
            ),
            Div(
                'auction_date', css_class="col-md-1",
            )
        )


    asset_type = django_filters.ChoiceFilter(choices=CATEGORIES_MAJOR,label='Asset type', method='filter_category')

    def filter_category(self, queryset, name, value):
        # construct the full lookup expression.
        cat = AssetType.objects.get(description=value).id
        cat_assets = AssetProperty.objects.filter(asset_type_id=cat).values_list('id')
        # print cat_assets['id']
        queryset = queryset.filter(asset_id__in=cat_assets)
        return queryset

    area = django_filters.ChoiceFilter(choices=areas,label="Area",method='filter_area')

    def filter_area(self, queryset, name, value):
        areas = GeoAreas.objects.get(name=value).id
        area_assets = AssetProperty.objects.filter(secondarea_id=areas).values_list('id')
        queryset = queryset.filter(asset_id__in=area_assets)
        return queryset

    starting_price = django_filters.NumberFilter(name='starting_price', lookup_expr='lt')

    auction_date = django_filters.ChoiceFilter(choices=dates_choices,label="Active",method='filter_auction_date')

    def filter_auction_date(self, queryset, name, value):
        date_today = datetime.date.today()
        print value
        if value=="1":
            queryset = queryset.filter(auction_date__gte=date_today)
        else:
            queryset = queryset.filter(auction_date__lt=date_today)

        return queryset
    # def get_queryset(self):
    #     # project_id may be None
    #     return self.queryset.filter(buy_or_rent=self.kwargs.get('buy_or_rent'))

    class Meta:
        model = TranAuction
        fields = ['asset_type','area','starting_price','auction_date']


class CommercialFilter(django_filters.FilterSet):

    def __init__(self, *args, **kwargs):

        super(CommercialFilter, self).__init__(*args, **kwargs)
        self.CATEGORIES_MINOR = []
        self.areas = []
        self.helper = FormHelper()
        self.helper.label_class = 'control-label'
        self.helper.field_class = 'selectpicker'
        self.helper.layout = Layout(
            Div(
                'asset_type', css_class="col-md-2",
            ),
            Div(
                'asset_type_minor', css_class="col-md-3",
            ),
            Div(
                'city', css_class="col-md-3",
            ),
            Div(
                'area', css_class="col-md-5",
            ),
            Div(
                'buy_or_rent', css_class="col-md-2",
            )
        )

        if self.request.GET.get('asset_type'):

            cat_minor = AssetType.objects.get(description=self.request.GET.get('asset_type')).synonyms
            # cat_minor = AssetType.objects.get(id=cat_id).synonyms
            # CATEGORIES_MINOR = [(x[0], x[0]) for x in y for y in cat_minor]

            self.CATEGORIES_MINOR.append(('', 'Any'))
            for y in cat_minor:
                self.CATEGORIES_MINOR.append((y, y))

            self.form.fields['asset_type_minor'].choices = self.CATEGORIES_MINOR


        if self.request.GET.get('city'):

            city_id = GeoCities.objects.get(name=self.request.GET.get('city'))
            areas = GeoAreas.objects.filter(city_id=city_id)
            # cat_minor = AssetType.objects.get(id=cat_id).synonyms
            # CATEGORIES_MINOR = [(x[0], x[0]) for x in y for y in cat_minor]

            self.areas.append(('', 'Any'))
            for y in areas:
                self.areas.append((y, y))

            self.form.fields['area'].choices = self.areas

    asset_type = django_filters.ChoiceFilter(choices=CATEGORIES_MAJOR,label='Major type', method='filter_major_category')

    def filter_major_category(self, queryset, name, value):
        # construct the full lookup expression.
        cat = AssetType.objects.get(description=value).id
        cat_assets = AssetProperty.objects.filter(asset_type_id=cat).values_list('id')
        queryset = queryset.filter(asset_id__in=cat_assets)
        return queryset


    asset_type_minor = django_filters.ChoiceFilter(choices=CATEGORIES_MINOR,label='Minor type', method='filter_minor_category')

    def filter_minor_category(self, queryset, name, value):
        # cat = AssetType.objects.filter(synonyms__contains=value)
        # print cat
        cat_assets = Asset.objects.filter(category_minor=value).values_list('id')
        # print cat_assets['id']
        queryset = queryset.filter(asset_id__in=cat_assets)
        return queryset

    city = django_filters.ChoiceFilter(choices=cities,label="City",method='filter_city')

    def filter_city(self, queryset, name, value):
        city = GeoCities.objects.get(name=value).id

        area_assets = AssetProperty.objects.filter(mainarea_id=city).values_list('id')
        # print cat_assets['id']
        queryset = queryset.filter(asset_id__in=area_assets)
        return queryset

    # area = django_filters.CharFilter(lookup_expr='icontains',label="Area")
    area = django_filters.ChoiceFilter(choices=areas,label="Area",method='filter_area')

    def filter_area(self, queryset, name, value):
        areas = GeoAreas.objects.get(name=value).id
        area_assets = AssetProperty.objects.filter(secondarea_id=areas).values_list('id')
        # print cat_assets['id']
        queryset = queryset.filter(asset_id__in=area_assets)
        return queryset

    buy = TranCommercial.objects.order_by().values_list('buy_or_rent').distinct()
    BUY_OR_RENT = [(x[0], x[0]) for x in buy]
    buy_or_rent = django_filters.ChoiceFilter(choices=BUY_OR_RENT,label="Buy or rent")

    def filter_buy_or_rent(self, queryset, name, value):
        queryset = queryset.filter(buy_or_rent=value)
        return queryset


    class Meta:
        model = TranCommercial
        fields = ['city','area','asset_type','asset_type_minor','buy_or_rent']
