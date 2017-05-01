from datetime import datetime

from django.core.exceptions import MultipleObjectsReturned, ValidationError
from django.db.models import Manager, Model
from django.db.models.base import ModelBase
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

from django.db import connection

def init_connection():
    db_conn = connection

    try:
        db_conn.autocommit = True
        c = db_conn.cursor()
    except OperationalError:
        connected = False

    return c

def update_search_sources_coops():
    cursor = init_connection()

    update = "INSERT into sources (source_text, last_crawled) \
    ( SELECT DISTINCT ON (a.source) a.source,a.imported_date \
      FROM auctionapp_auction as a \
      ORDER BY a.source, a.imported_date DESC NULLS LAST \
    ); \
    INSERT into cooperator (contact_legal_name, contact_name, contact_phone, contact_email, contact_website) \
    ( \
    SELECT DISTINCT contact_legal_name, contact_name, contact_phone, contact_email, contact_website \
    from auctionapp_auction \
    ); \
    INSERT into search_info (imported_date) \
    (SELECT DISTINCT(a.imported_date) \
    from auctionapp_auction as a \
    );"

    cursor.execute(update)

def delete_search_sources_coops():
    cursor = init_connection()
    delete_query = "TRUNCATE TABLE sources CASCADE; \
    ALTER SEQUENCE sources_id_seq RESTART WITH 1; TRUNCATE TABLE cooperator CASCADE; \
    ALTER SEQUENCE cooperator_id_seq RESTART WITH 1; TRUNCATE TABLE search_info CASCADE; \
    ALTER SEQUENCE search_info_id_seq RESTART WITH 1; "
    cursor.execute(delete_query)


def update_transactions():
    cursor = init_connection()

    update_trans = "INSERT into tran_commercial \
    (search_id,asset_id,title,url,contact_legal_id,contact_website,source_id,on_site_date,selling_price,buy_or_rent) \
    (SELECT s.id, ass.id, a.title, a.url, co.id, co.contact_website, so.id, a.on_site_date, a.price_num, a.property_buy_or_rent \
    from auctionapp_auction as a, search_info as s, sources as so, asset as ass, cooperator as co \
    where ass.unique_id=a.unique_id and ass.title=a.title and a.source=so.source_text and \
    s.imported_date=a.imported_date and a.contact_website=co.contact_website \
    ) on conflict do nothing;"

    cursor.execute(update_trans)

def delete_transactions():
    cursor = init_connection()
    delete_query = "TRUNCATE TABLE transaction CASCADE; \
    ALTER SEQUENCE transaction_id_seq RESTART WITH 1;"

    cursor.execute(delete_query)


def update_properties():
    cursor = init_connection()

    update_prop_res = "INSERT into prop_residential (title,mainarea_id,secondarea_id,address,asset_type,img_url, \
    unique_id,status,updated_date,embadon,other,longitude,latitude,bedrooms,construction_year) ( \
    SELECT a.title,g.city_id,g.id,a.address,t.id,a.img_url,a.unique_id,'',now(),a.property_area_num,a.description,g.longitude,g.latitude,a.property_rooms_num,a.construction_year \
    from auctionapp_auction as a, geo_areas as g, asset_property_type as t \
    where (a.asset_type='realestate' or a.asset_type='real estate') and a.category_major='residential' and CONCAT(a.neighborhood,', ',trim((string_to_array(a.region,'-'))[1]),', Greece')=ANY(g.crawled_names) and a.category_minor=ANY(t.synonyms) \
    )on conflict do nothing;"

    cursor.execute(update_prop_res)

    update_prop_comm = "INSERT into prop_commercial (title,mainarea_id,secondarea_id, address,asset_type,img_url, \
    unique_id,status,updated_date,embadon,other,longitude,latitude,rooms,construction_year) ( SELECT \
    a.title,g.city_id,g.id,a.address,t.id,a.img_url,a.unique_id,'',now(),a.property_area_num,a.description,a.longitude,a.latitude,a.property_rooms_num,a.construction_year \
    from auctionapp_auction as a, geo_areas as g, asset_property_type as t \
    where (a.asset_type='realestate' or a.asset_type='real estate') and a.category_major='commercial' and \
    CONCAT(a.neighborhood,', ',trim((string_to_array(a.region,'-'))[1]),', Greece')=ANY(g.crawled_names) and \
    a.category_minor=ANY(t.synonyms) \
    )on conflict do nothing;"

    cursor.execute(update_prop_comm)

    update_prop_land = "INSERT into prop_earth (title,mainarea_id,secondarea_id,address, asset_type,img_url, unique_id,status,updated_date,size,other,longitude,latitude,inmap) ( SELECT a.title,g.city_id,g.id,a.address,t.id,a.img_url,a.unique_id,'',now(),a.property_area_num,a.description,g.longitude,g.latitude,'' from auctionapp_auction as a, geo_areas as g, asset_property_type as t where (a.asset_type='realestate' or a.asset_type='real estate') and a.category_major='land' and CONCAT(a.neighborhood,', ',trim((string_to_array(a.region,'-'))[1]),', Greece')=ANY(g.crawled_names) and a.category_minor=ANY(t.synonyms) )on conflict do nothing;"

    cursor.execute(update_prop_land)

def delete_properties():
    cursor = init_connection()
    delete_query = "TRUNCATE TABLE asset CASCADE; \
    ALTER SEQUENCE asset_id_seq RESTART WITH 1; "

    cursor.execute(delete_query)
