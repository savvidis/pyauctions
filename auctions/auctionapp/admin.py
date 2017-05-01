from django.contrib import admin
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View


def update_database(request, *args, **kwargs):
    # return HttpResponse("Hello!")
    return HttpResponseRedirect("synchro.html")

admin.site.register_view('auctionapp/synchro.html', view=update_database, name='Update database')

# Register your models here.

class AuctionAdmin(admin.ModelAdmin):
    # list_display  = [f.name for f in Auction._meta.fields]
    list_display = ('id','asset_type', 'transaction_type', 'imported_date', 'source', 'url', \
    'img_url', 'unique_id', 'title')
admin.site.register(Auction,AuctionAdmin)

class AssetAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in Asset._meta.fields]
admin.site.register(Asset,AssetAdmin)

class AssetCarAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in AssetCar._meta.fields]
admin.site.register(AssetCar,AssetCarAdmin)

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

class SearchInfoAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in SearchInfo._meta.fields]
admin.site.register(SearchInfo,SearchInfoAdmin)

class SourcesAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in Sources._meta.fields]
admin.site.register(Sources,SourcesAdmin)

class TranAuctionAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in TranAuction._meta.fields]
admin.site.register(TranAuction,TranAuctionAdmin)

class TranCommercialAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in TranCommercial._meta.fields]
admin.site.register(TranCommercial,TranCommercialAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in Transaction._meta.fields]
admin.site.register(Transaction,TransactionAdmin)
