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
    # About the entry (Seperate table)
    asset_type = models.CharField(null=True, default="", max_length=255)  # Car / Properties
    transaction_type = models.CharField(null=True, default="", max_length=255)  # Buy / Sell / Auction
    # slug = models.SluygField(editable=False, unique=True)
    imported_date = models.DateField(null=True, editable=False, default=timezone.now())
    source = models.CharField(null=True, editable=False, default="", max_length=255)
    url = models.URLField(max_length=250, blank=True)
    img_url = models.URLField(null=True, max_length=250, blank=True)
    # About Asset (Seperate table)
    unique_id = models.CharField(null=True, editable=False, default="", max_length=255)
    title = models.CharField(null=True, max_length=255)
    category = models.CharField(null=True, default="", max_length=255)
    description = models.TextField(null=True, default="")
    construction_year_num = models.IntegerField(null=True, default=0)
    price_num = models.IntegerField(null=True, default=-1)
    views_num = models.IntegerField(null=True, default=-1)
    # About Location
    city = models.CharField(null=True, default="", max_length=255)
    region = models.CharField(null=True, editable=True, default="", max_length=255)
    address = models.CharField(null=True, editable=True, default="", max_length=255)
    neighborhood = models.CharField(null=True, editable=True, default="", max_length=255)
    longitude = models.FloatField(null=True, default=0)
    latitude = models.FloatField(null=True, default=0)

    # About Timing
    on_site_date = models.DateField(null=True, default=datetime(2010, 1, 1, 1, 10))
    updated_date = models.DateField(null=True, default=datetime(2010, 1, 1, 1, 10))
    last_update_num = models.IntegerField(null=True, default=-1)
    # Asset Specific if property or car
    property_area_num = models.IntegerField(null=True, default=-1)
    property_rooms_num = models.IntegerField(null=True, default=-1)
    property_buy_or_rent = models.CharField(null=True, default="", max_length=255)
    car_kms_num = models.IntegerField(null=True, default=-1)
    car_cc_num = models.IntegerField(null=True, default=-1)
    car_fuel = models.CharField(null=True, editable=False, default="", max_length=255)
    # Specific if Auction
    debtor_name = models.CharField(null=True, default="n/a", max_length=255)
    auctioneer_name = models.CharField(null=True, default="n/a", max_length=255)
    auction_date = models.DateField(null=True, default=datetime(2010, 1, 1, 1, 10))
    auction_number = models.IntegerField(editable=False, null=True, default=0)
    # Contact Information (Seperate table)
    contact_legal_name = models.CharField(default="", null=True, max_length=255)
    contact_name = models.CharField(default="", null=True, max_length=255)
    contact_phone = models.CharField(default="", null=True, max_length=255)
    contact_mobile = models.CharField(default="", null=True, max_length=255)
    contact_email = models.EmailField(default="", null=True, max_length=255)
    contact_website = models.URLField(default="", null=True, max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = (
            ("title", "asset_type"),
        )
