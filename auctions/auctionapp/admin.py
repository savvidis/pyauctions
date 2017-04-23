from django.contrib import admin
from .models import *
from django.http import HttpResponse

def my_view(request, *args, **kwargs):
    return HttpResponse("Hello!")

admin.site.register_view('somepath', view=my_view)

# Register your models here.

class AuctionAdmin(admin.ModelAdmin):
    # list_display  = [f.name for f in Auction._meta.fields]
    list_display = ('id','asset_type', 'transaction_type', 'imported_date', 'source', 'url', \
    'img_url', 'unique_id', 'title')
admin.site.register(Auction,AuctionAdmin)

admin.site.register(Source)

admin.site.register(Asset)
admin.site.register(AssetCar)
admin.site.register(AssetProperty)

class AssetPropertyTypeAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in AssetPropertyType._meta.fields]
admin.site.register(AssetPropertyType,AssetPropertyTypeAdmin)

class CooperatorAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in Cooperator._meta.fields]
admin.site.register(Cooperator,CooperatorAdmin)

class GeoAreasAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in GeoAreas._meta.fields]
admin.site.register(GeoAreas,GeoAreasAdmin)

class GeoCityAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in GeoCity._meta.fields]
admin.site.register(GeoCity,GeoCityAdmin)

class GeoCountriesAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in GeoCountries._meta.fields]
admin.site.register(GeoCountries,GeoCountriesAdmin)

class GeoRegionsAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in GeoRegions._meta.fields]
admin.site.register(GeoRegions,GeoRegionsAdmin)

class PropCommercialAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in PropCommercial._meta.fields]
admin.site.register(PropCommercial,PropCommercialAdmin)

class PropEarthAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in PropEarth._meta.fields]
admin.site.register(PropEarth,PropEarthAdmin)

class PropResidentialAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in PropResidential._meta.fields]
admin.site.register(PropResidential,PropResidentialAdmin)

admin.site.register(SearchInfo)
admin.site.register(Sources)
admin.site.register(TranAuction)
admin.site.register(TranCommercial)
admin.site.register(Transaction)
