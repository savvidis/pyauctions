from django.shortcuts import render
from auctions.auctionapp.models import *
from django.core import serializers
import json
from django.core.serializers import serialize
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, YourCustomType):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)

def start(request):
    """Start page with a documentation.
    """
    return render(request, "django_sb_admin/start.html",{"nav_active":"start"})

def dashboard(request):
    """Dashboard page.
    """
    places_count = AssetProperty.objects.count()
    asset_residential_count = PropResidential.objects.count()
    asset_commercial_count = PropCommercial.objects.count()
    asset_earth_count = PropEarth.objects.count()

    searchinfo = serialize('json', SearchInfo.objects.all())
    searchinfo = json.dumps(searchinfo)

    return render(request, "django_sb_admin/sb_admin_dashboard.html",
                  {"nav_active":"dashboard",'places_count': places_count,'asset_residential_count': asset_residential_count,
                  'asset_commercial_count':asset_commercial_count,'asset_earth_count':asset_earth_count,'searchinfo':searchinfo})


def charts(request):
    """Charts page.
    """
    return render(request, "django_sb_admin/sb_admin_charts.html", {"nav_active":"charts"})

def tables(request):
    """Tables page.
    """
    return render(request, "django_sb_admin/sb_admin_tables.html", {"nav_active":"tables"})

def forms(request):
    """Forms page.
    """
    return render(request, "django_sb_admin/sb_admin_forms.html", {"nav_active":"forms"})

def bootstrap_elements(request):
    """Bootstrap elements page.
    """
    return render(request, "django_sb_admin/sb_admin_bootstrap_elements.html", {"nav_active":"bootstrap_elements"})
    
def bootstrap_grid(request):
    """Bootstrap grid page.
    """
    return render(request, "django_sb_admin/sb_admin_bootstrap_grid.html",
                  {"nav_active":"bootstrap_grid"})

def dropdown(request):
    """Dropdown  page.
    """
    return render(request, "django_sb_admin/sb_admin_dropdown.html",
                  {"nav_active":"dropdown"})

def rtl_dashboard(request):
    """RTL Dashboard page.
    """
    return render(request, "django_sb_admin/sb_admin_rtl_dashboard.html",
                  {"nav_active":"rtl_dashboard"})

def blank(request):
    """Blank page.
    """
    return render(request, "django_sb_admin/sb_admin_blank.html",
                  {"nav_active":"blank"})
