from django.db import models
from datetime import datetime
from django.utils import timezone

from django.contrib.postgres.fields import ArrayField

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
    asset_type = models.CharField(
        null=True, default="", max_length=255)  # Car / Properties
    transaction_type = models.CharField(
        null=True, default="", max_length=255)  # Buy / Sell / Auction
    # slug = models.SluygField(editable=False, unique=True)
    imported_date = models.DateField(
        null=True, editable=False, default=timezone.now)
    source = models.CharField(
        null=True, editable=False, default="", max_length=255)
    url = models.URLField(max_length=250, blank=True)
    img_url = models.URLField(null=True, max_length=250, blank=True)
    # About Asset (Seperate table)
    unique_id = models.CharField(
        null=True, editable=False, default="", max_length=255)
    title = models.CharField(null=True, max_length=255)
    category_major = models.CharField(null=True, default="", max_length=255)
    category_minor = models.CharField(null=True, default="", max_length=255)
    description = models.TextField(null=True, default="")
    construction_year = models.CharField(null=True, default="", max_length=255)
    price_num = models.IntegerField(null=True, default=-1)
    views_num = models.IntegerField(null=True, default=-1)
    # About Location
    city = models.CharField(null=True, default="", max_length=255)
    region = models.CharField(null=True, editable=True,
                              default="", max_length=255)
    address = models.CharField(
        null=True, editable=True, default="", max_length=255)
    neighborhood = models.CharField(
        null=True, editable=True, default="", max_length=255)
    longitude = models.FloatField(null=True, default=0)
    latitude = models.FloatField(null=True, default=0)
    fulltext = models.TextField(null=True, default="")
    other1 = models.TextField(null=True, default="")
    other1_num = models.IntegerField(null=True, default=-1)
    other2 = models.TextField(null=True, default="")
    other2_num = models.IntegerField(null=True, default=-1)

    # About Timing
    on_site_date = models.DateField(
        null=True, default=timezone.now)
    updated_date = models.DateField(
        null=True, default=timezone.now)
    last_update_num = models.IntegerField(null=True, default=-1)
    # Asset Specific if property or car
    property_area_num = models.IntegerField(null=True, default=-1)
    property_rooms_num = models.IntegerField(null=True, default=-1)
    property_buy_or_rent = models.CharField(
        null=True, default="", max_length=255)
    car_kms_num = models.IntegerField(null=True, default=-1)
    car_cc_num = models.IntegerField(null=True, default=-1)
    car_fuel = models.CharField(
        null=True, editable=False, default="", max_length=255)
    # Specific if Auction
    debtor_name = models.CharField(null=True, default="n/a", max_length=255)
    auctioneer_name = models.CharField(
        null=True, default="n/a", max_length=255)
    auction_date = models.DateField(
        null=True, default=timezone.now)
    auction_number = models.IntegerField(editable=False, null=True, default=0)
    # Contact Information (Seperate table)
    contact_legal_name = models.CharField(
        default="", null=True, max_length=255)
    contact_name = models.CharField(default="", null=True, max_length=255)
    contact_phone = models.CharField(default="", null=True, max_length=255)
    contact_mobile = models.CharField(default="", null=True, max_length=255)
    contact_email = models.EmailField(default="", null=True, max_length=255)
    contact_website = models.URLField(default="", null=True, max_length=255)

    def __str__(self):
        return self.url

    class Meta:
        unique_together = (
            ("title", "asset_type"),
        )

class Asset(models.Model):
    title = models.CharField(max_length=250, blank=True, null=True)
    mainarea_id = models.IntegerField(blank=True, null=True)
    secondarea = models.CharField(max_length=150, blank=True, null=True)
    percentage = models.CharField(max_length=150, blank=True, null=True)
    img_url = models.CharField(max_length=250, blank=True, null=True)
    unique_id = models.CharField(max_length=250, blank=True, null=True)
    performance_category = models.CharField(max_length=250, blank=True, null=True)
    suggest_price = models.FloatField(blank=True, null=True)
    suggest_income = models.FloatField(blank=True, null=True)
    category_major = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    updated_date = models.DateField(blank=True, null=True)
    profit_loss_income = models.FloatField(blank=True, null=True)
    full_text = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asset'


class AssetCar(models.Model):
    title = models.CharField(max_length=250, blank=True, null=True)
    mainarea_id = models.IntegerField(blank=True, null=True)
    secondarea = models.CharField(max_length=150, blank=True, null=True)
    percentage = models.CharField(max_length=150, blank=True, null=True)
    img_url = models.CharField(max_length=250, blank=True, null=True)
    unique_id = models.CharField(max_length=250, blank=True, null=True)
    performance_category = models.CharField(max_length=250, blank=True, null=True)
    suggest_price = models.FloatField(blank=True, null=True)
    suggest_income = models.FloatField(blank=True, null=True)
    category_major = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    updated_date = models.DateField(blank=True, null=True)
    profit_loss_income = models.FloatField(blank=True, null=True)
    car_kms_num = models.IntegerField(blank=True, null=True)
    car_cc_num = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    first_hand = models.NullBooleanField()
    other = models.TextField(blank=True, null=True)
    fuel_type = models.CharField(max_length=150, blank=True, null=True)
    full_text = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asset_car'


class AssetProperty(models.Model):
    title = models.CharField(max_length=250, blank=True, null=True)
    mainarea_id = models.IntegerField(blank=True, null=True)
    secondarea = models.CharField(max_length=150, blank=True, null=True)
    percentage = models.CharField(max_length=150, blank=True, null=True)
    img_url = models.CharField(max_length=250, blank=True, null=True)
    unique_id = models.CharField(max_length=250, blank=True, null=True)
    performance_category = models.CharField(max_length=250, blank=True, null=True)
    suggest_price = models.FloatField(blank=True, null=True)
    suggest_income = models.FloatField(blank=True, null=True)
    category_major = models.CharField(max_length=250, blank=True, null=True)
    category_minor = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    updated_date = models.DateField(blank=True, null=True)
    profit_loss_income = models.FloatField(blank=True, null=True)
    embadon = models.FloatField(blank=True, null=True)
    other = models.TextField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    asset_type = models.CharField(max_length=20, blank=True, null=True)
    full_text = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asset_property'


class AssetPropertyType(models.Model):
    description = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asset_property_type'


class Cooperator(models.Model):
    contact_legal_name = models.CharField(max_length=250, blank=True, null=True)
    contact_name = models.CharField(max_length=250, blank=True, null=True)
    contact_phone = models.CharField(max_length=250, blank=True, null=True)
    contact_mobile = models.CharField(max_length=250, blank=True, null=True)
    contact_email = models.CharField(max_length=250, blank=True, null=True)
    contact_website = models.CharField(max_length=250, blank=True, null=True)
    coo_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cooperator'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class GeoAreas(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    postcode = models.CharField(max_length=250, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    city = models.ForeignKey('GeoCity', models.DO_NOTHING, blank=True, null=True)
    # crawled_names = models.TextField(blank=True, null=True)  # This field type is a guess.
    crawled_names = ArrayField(models.CharField(max_length=150, blank=True))

    class Meta:
        managed = False
        db_table = 'geo_areas'

    def __unicode__(self):
        return "%s" % self.name


class GeoCity(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    region = models.ForeignKey('GeoRegions', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geo_city'

    def __unicode__(self):
        return "%s" % self.name

class GeoCountries(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geo_countries'


class GeoRegions(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    country = models.ForeignKey(GeoCountries, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geo_regions'

    def __unicode__(self):
        return "%s" % self.name


class PropCommercial(models.Model):
    title = models.CharField(max_length=250, blank=True, null=True)
    mainarea_id = models.IntegerField(blank=True, null=True)
    secondarea = models.CharField(max_length=150, blank=True, null=True)
    percentage = models.CharField(max_length=150, blank=True, null=True)
    img_url = models.CharField(max_length=250, blank=True, null=True)
    unique_id = models.CharField(max_length=250, blank=True, null=True)
    performance_category = models.CharField(max_length=250, blank=True, null=True)
    suggest_price = models.FloatField(blank=True, null=True)
    suggest_income = models.FloatField(blank=True, null=True)
    category_major = models.CharField(max_length=250, blank=True, null=True)
    category_minor = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    updated_date = models.DateField(blank=True, null=True)
    profit_loss_income = models.FloatField(blank=True, null=True)
    embadon = models.FloatField(blank=True, null=True)
    other = models.TextField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    asset_type = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=150, blank=True, null=True)
    construction_year = models.CharField(max_length=250, blank=True, null=True)
    full_text = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prop_commercial'


class PropEarth(models.Model):
    title = models.CharField(max_length=250, blank=True, null=True)
    mainarea_id = models.IntegerField(blank=True, null=True)
    secondarea = models.CharField(max_length=150, blank=True, null=True)
    percentage = models.CharField(max_length=150, blank=True, null=True)
    img_url = models.CharField(max_length=250, blank=True, null=True)
    unique_id = models.CharField(max_length=250, blank=True, null=True)
    performance_category = models.CharField(max_length=250, blank=True, null=True)
    suggest_price = models.FloatField(blank=True, null=True)
    suggest_income = models.FloatField(blank=True, null=True)
    category_major = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    updated_date = models.DateField(blank=True, null=True)
    profit_loss_income = models.FloatField(blank=True, null=True)
    embadon = models.FloatField(blank=True, null=True)
    other = models.TextField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    asset_type = models.CharField(max_length=20, blank=True, null=True)
    inmap = models.CharField(max_length=50, blank=True, null=True)
    size = models.FloatField(blank=True, null=True)
    full_text = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prop_earth'


class PropResidential(models.Model):
    title = models.CharField(max_length=250, blank=True, null=True)
    mainarea_id = models.IntegerField(blank=True, null=True)
    secondarea = models.CharField(max_length=150, blank=True, null=True)
    percentage = models.CharField(max_length=150, blank=True, null=True)
    img_url = models.CharField(max_length=250, blank=True, null=True)
    unique_id = models.CharField(max_length=250, blank=True, null=True)
    performance_category = models.CharField(max_length=250, blank=True, null=True)
    suggest_price = models.FloatField(blank=True, null=True)
    suggest_income = models.FloatField(blank=True, null=True)
    category_major = models.CharField(max_length=250, blank=True, null=True)
    category_minor = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    updated_date = models.DateField(blank=True, null=True)
    profit_loss_income = models.FloatField(blank=True, null=True)
    embadon = models.FloatField(blank=True, null=True)
    other = models.TextField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    asset_type = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=150, blank=True, null=True)
    bedrooms = models.CharField(max_length=100, blank=True, null=True)
    construction_year = models.CharField(max_length=250, blank=True, null=True)
    full_text = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prop_residential'


class SearchInfo(models.Model):
    imported_date = models.DateField(blank=True, null=True)
    category_id = models.IntegerField()
    nomos_id = models.IntegerField()
    source_id = models.IntegerField()
    isoffer = models.NullBooleanField()
    issold = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'search_info'


class Sources(models.Model):
    source_text = models.TextField(blank=True, null=True)
    last_crawled = models.DateField(blank=True, null=True)
    source_type = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sources'


class TranAuction(models.Model):
    search_id = models.IntegerField(blank=True, null=True)
    asset_id = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=250, blank=True, null=True)
    url = models.CharField(max_length=250, blank=True, null=True)
    contact_legal_id = models.IntegerField(blank=True, null=True)
    contact_website = models.CharField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=250)
    source_id = models.IntegerField(blank=True, null=True)
    starting_price = models.FloatField(blank=True, null=True)
    onsight_date = models.DateField(blank=True, null=True)
    debtor_name = models.CharField(max_length=150, blank=True, null=True)
    creditor_name = models.CharField(max_length=150, blank=True, null=True)
    auction_number = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tran_auction'


class TranCommercial(models.Model):
    search_id = models.IntegerField(blank=True, null=True)
    asset_id = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=250, blank=True, null=True)
    url = models.CharField(max_length=250, blank=True, null=True)
    contact_legal_id = models.IntegerField(blank=True, null=True)
    contact_website = models.CharField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=250)
    source_id = models.IntegerField(blank=True, null=True)
    on_site_date = models.DateField(blank=True, null=True)
    selling_price = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tran_commercial'


class Transaction(models.Model):
    search = models.ForeignKey(SearchInfo, models.DO_NOTHING, blank=True, null=True)
    asset = models.ForeignKey(Asset, models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=250, blank=True, null=True)
    url = models.CharField(max_length=250, blank=True, null=True)
    contact_legal = models.ForeignKey(Cooperator, models.DO_NOTHING, blank=True, null=True)
    contact_website = models.CharField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=250)
    source = models.ForeignKey(Sources, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transaction'
