# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


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
    id = models.AutoField()
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
    id = models.AutoField()
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


class AuctionappAuction(models.Model):
    id = models.AutoField(blank=True, null=True)
    asset_type = models.CharField(max_length=255, blank=True, null=True)
    transaction_type = models.CharField(max_length=255, blank=True, null=True)
    imported_date = models.DateField(blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=250)
    img_url = models.CharField(max_length=250, blank=True, null=True)
    unique_id = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    category_major = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    construction_year = models.CharField(max_length=255, blank=True, null=True)
    price_num = models.IntegerField(blank=True, null=True)
    views_num = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    neighborhood = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    on_site_date = models.DateField(blank=True, null=True)
    updated_date = models.DateField(blank=True, null=True)
    last_update_num = models.IntegerField(blank=True, null=True)
    property_area_num = models.IntegerField(blank=True, null=True)
    property_rooms_num = models.IntegerField(blank=True, null=True)
    property_buy_or_rent = models.CharField(max_length=255, blank=True, null=True)
    car_kms_num = models.IntegerField(blank=True, null=True)
    car_cc_num = models.IntegerField(blank=True, null=True)
    car_fuel = models.CharField(max_length=255, blank=True, null=True)
    debtor_name = models.CharField(max_length=255, blank=True, null=True)
    auctioneer_name = models.CharField(max_length=255, blank=True, null=True)
    auction_date = models.DateField(blank=True, null=True)
    auction_number = models.IntegerField(blank=True, null=True)
    contact_legal_name = models.CharField(max_length=255, blank=True, null=True)
    contact_name = models.CharField(max_length=255, blank=True, null=True)
    contact_phone = models.CharField(max_length=255, blank=True, null=True)
    contact_mobile = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.CharField(max_length=255, blank=True, null=True)
    contact_website = models.CharField(max_length=255, blank=True, null=True)
    category_minor = models.CharField(max_length=255, blank=True, null=True)
    fulltext = models.TextField(blank=True, null=True)
    other1 = models.TextField(blank=True, null=True)
    other1_num = models.IntegerField(blank=True, null=True)
    other2 = models.TextField(blank=True, null=True)
    other2_num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auctionapp_auction'


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
    crawled_names = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'geo_areas'


class GeoCity(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    region = models.ForeignKey('GeoRegions', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geo_city'


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


class PropCommercial(models.Model):
    id = models.AutoField()
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
    type = models.CharField(max_length=150, blank=True, null=True)
    construction_year = models.CharField(max_length=250, blank=True, null=True)
    full_text = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prop_commercial'


class PropEarth(models.Model):
    id = models.AutoField()
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
    id = models.AutoField()
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
    id = models.AutoField()
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
    id = models.AutoField()
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
