from django.conf import settings
from django_hosts import host

print(settings.ROOT_URLCONF)
host_patterns = [
    host(r'127.0.0.1:8000', settings.ROOT_URLCONF, name='www'),
    # host(r'docs', 'djangoproject.urls.docs', name='docs'),
    # host(r'dashboard', 'dashboard.urls', name='dashboard'),
]
