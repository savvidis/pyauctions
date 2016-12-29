# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from .views import *

urlpatterns = [
    url(
        regex=r'^$',
        view=AuctionListView.as_view(),
        name='list'
    ),
    url(
        regex=r'^(?P<asset_type>[A-Za-z]+)/$',
        view=AuctionTypeView.as_view(),
        name='type'
    ),
    # url(
    #     regex=r'[.+][\?q=\/][.*]$',
    #     view=AuctionFormView.as_view(),
    #     name='form'
    # ),
    # url(
    #     regex=r'^(?P<asset_type>[A-Za-z&]*)$',

    #     regex=r'^~redirect/$',
    #     view=views.UserRedirectView.as_view(),
    #     name='redirect'
    # ),
    url(
        regex=r'^(?P<pk>[\d.@+-]+)/$',
        view=AuctionDetailView.as_view(),
        name='detail'
    ),
    # url(
    #     regex=r'^~update/$',
    #     view=views.UserUpdateView.as_view(),
    #     name='update'
    # ),
]
