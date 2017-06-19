# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.views import defaults as default_views

from django.contrib import admin
from adminplus.sites import AdminSitePlus

import auctions.django_sb_admin

admin.site = AdminSitePlus()
admin.autodiscover()

from auctions.auctionapp.views import *

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),

    # url(r'^admin/auctionapp/', TemplateView.as_view(template_name='auctionapp/synchro.html')),
    url(r'^admin/auctionapp/synchro.html', synchro, name='synchro'),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # User management
    url(r'^users/', include('auctions.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),

    # Your stuff: custom urls includes go here
    url(r'^blog/', include('auctions.blog.urls', namespace='blog')),
    url(r'^search/', include('auctions.auctionapp.urls', namespace='auctionapp')),

    url(r'^django-sb-admin/', include('auctions.django_sb_admin.urls')),
    url(r'^accounts/login/$', auth_views.login,{'template_name': 'django_sb_admin/examples/login.html'}),

    url(
        regex=r'^cities-autocomplete/$',
        view=GeoCitiesAutocomplete.as_view(),
        name='cities-autocomplete',
    ),

    url(
        regex=r'^areas-autocomplete/$',
        view=GeoAreasAutocomplete.as_view(),
        name='areas-autocomplete',
    ),

    url(r'^admin/', include(admin.site.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request,
            kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied,
            kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found,
            kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
