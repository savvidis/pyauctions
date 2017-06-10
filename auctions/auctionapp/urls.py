# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url,include

from .views import *

urlpatterns = [
    # url(
    #     regex=r'^$',
    #     view=AuctionListView.as_view(),
    #     name='list'
    # ),
    # url(
    #     regex=r'^(?P<asset_type>[A-Za-z]+)/$',
    #     view=AuctionTypeView.as_view(),
    #     name='type'
    # ),
    # url(
    #     regex=r'^(?P<pk>[\d.@+-]+)/$',
    #     view=AuctionDetailView.as_view(),
    #     name='detail'
    # ),
    url(
        regex=r'^auction/$',
        view=AuctionListView.as_view(),
        name='auction_list'
    ),
    url(
        regex=r'^realestate/$',
        view=CommercialListView.as_view(),
        name='commercial_list'
    ),
    url(regex=r'^auction/(?P<pk>[0-9]+)/$', view=AuctionDetailView.as_view(), name='auction_detail'),
    url(regex=r'^realestate/(?P<pk>[0-9]+)/$', view=CommercialDetailView.as_view(), name='commercial_detail'),
    url(r'^django-sb-admin/', include('auctions.django_sb_admin.urls')),
    url(
        regex=r'^country-autocomplete/$',
        view=CountryAutocomplete.as_view(),
        name='country-autocomplete',
    ),
    # url(
    #     regex=r'^~update/$',
    #     view=views.UserUpdateView.as_view(),
    #     name='update'
    # ),
]
