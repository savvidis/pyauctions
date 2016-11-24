from django.db import models
from datetime import datetime
from django.utils import timezone

# Create your models here.
# from auctions.auctionapp.models import *
# t = Type(**TypeDemo)
# a = Auction(**AssetDemo)


TYPE_OF_ASSETS = ((1, 'Real estate'), (2, 'Cars'))
TYPE_OF_SOURCES = ((1, 'Bank'), (2, 'Leasing'))


class Type(models.Model):
    asset_type = models.CharField(max_length=255)

    def __str__(self):
        return self.asset_type


class Source(models.Model):
    source_site = models.URLField(max_length=255)
    source_name = models.CharField(default="", max_length=255)
    source_type = models.IntegerField(default=1, choices=TYPE_OF_SOURCES)

    def __str__(self):
        return self.source_site


class Auction(models.Model):
    unique_code = models.CharField(editable=False, default="", max_length=255)
    # slug = models.SlugField(editable=False, unique=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date_imported = models.DateField(editable=False, default=timezone.now())
    asset_type = models.IntegerField(choices=TYPE_OF_ASSETS)
    # Details about the asset
    asset_city = models.CharField(default="", max_length=255)
    asset_zip = models.CharField(editable=False, default="", max_length=255)
    asset_address = models.CharField(editable=False, default="", max_length=255)
    debtor_name = models.CharField(default="None", max_length=255)
    debtor_vat_number = models.CharField(editable=False, default="", max_length=255)
    auctioneer_name = models.CharField(max_length=255)
    auctioneer_vat_number = models.CharField(editable=False, default="", max_length=255)
    offer_price = models.IntegerField(default=-1)
    published_date = models.DateField(default=datetime(2010, 1, 1, 1, 10))
    auction_date = models.DateField(default=datetime(2010, 1, 1, 1, 10))
    description = models.TextField(default="")
    auction_num = models.IntegerField(editable=False, default=1)
    auction_url = models.URLField("URL", max_length=250, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            ("name", "asset_type"),
        )
