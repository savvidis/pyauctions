# -*- coding: utf-8 -*-
"""
Local settings

- Run in Debug mode

- Use console backend for emails

- Add Django Debug Toolbar
- Add django-extensions as app
"""

import socket
import os
from .common import *  # noqa

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY', default='fe6bi(a%na7y=9#!w+h0j*697e7+ol0ue)g3d#zd=0jdi%kr^5')

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'wid_db',
    #     'USER': 'dascim',
    #     'PASSWORD': 'l1x#T3am',
    #     'HOST': 'wid-data-dev.chnsziqcpidr.eu-west-1.rds.amazonaws.com',
    #     'PORT': 5432
    # },
    # 'remote': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'wid_db',
    #     'USER': 'dascim',
    #     'PASSWORD': 'l1x#T3am',
    #     'HOST': 'wid-data-ie.chnsziqcpidr.eu-west-1.rds.amazonaws.com',
    #     'PORT': 5432
    # }
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     'auctions',
        'USER':     'postgres',
        'PASSWORD': 'Dbt2bvrgef',
        'HOST':     'localhost',
        'PORT': 5432
    },
}

# Mail settings
# ------------------------------------------------------------------------------

EMAIL_PORT = 1025

EMAIL_HOST = 'localhost'
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
                    default='django.core.mail.backends.console.EmailBackend')


# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS += ('debug_toolbar', )

INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]
# tricks to have debug toolbar when developing with docker
if os.environ.get('USE_DOCKER') == 'yes':
    ip = socket.gethostbyname(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + "1"]

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ('django_extensions', )

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Added

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['www', '127.0.0.1', 'testpage.eu'])

# Your local stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------

DEFAULT_HOST = 'www'

HOST_SCHEME = 'http'

HOST_SITE_TIMEOUT = 3600

ROOT_HOSTCONF = 'config.hosts'
