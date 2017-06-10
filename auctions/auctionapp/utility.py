from datetime import datetime

from django.core.exceptions import MultipleObjectsReturned, ValidationError
from django.db.models import Manager, Model
from django.db.models.base import ModelBase
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

from django.db import connection

import googlemaps
from datetime import datetime
import psycopg2
import pandas as pd
import math
import numpy as np

from os.path import dirname

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
    INSERT into auctioneer (name) \
    ( \
    SELECT DISTINCT auctioneer_name \
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

    update_trans = "INSERT into tran_auction (search_id,asset_id,title,url,contact_legal_id,source_id,starting_price,on_site_date,auction_date, debtor_name,auctioneer_name, auction_number,fulltext) \
    (SELECT s.id, ass.id, a.title, a.url, auc.id, so.id,a.price_num, a.on_site_date, a.auction_date, a.debtor_name, a.auctioneer_name, a.auction_number,a.fulltext \
    from auctionapp_auction as a, search_info as s, sources as so, asset as ass, auctioneer as auc \
    where a.transaction_type='auction' and s.id=2 and ass.title=a.title and a.source=so.source_text and auc.name=a.auctioneer_name \
    ) on conflict do nothing;"

    cursor.execute(update_trans)

    update_trans = "INSERT into tran_commercial \
    (search_id,asset_id,title,url,contact_legal_id,contact_website,source_id,on_site_date,selling_price,buy_or_rent) \
    (SELECT s.id, ass.id, a.title, a.url, co.id, co.contact_website, so.id, a.on_site_date, a.price_num, a.property_buy_or_rent \
    from auctionapp_auction as a, search_info as s, sources as so, asset as ass, cooperator as co \
    where a.transaction_type='commercial' and ass.title=a.title and a.source=so.source_text and \
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

    update_prop_land = "INSERT into prop_earth (title,mainarea_id,secondarea_id,address, asset_type_id,category_minor,img_url, unique_id,status,updated_date,size,other,longitude,latitude,inmap) ( \
    SELECT a.title,g.city_id,g.id,a.address,t.id,a.category_minor,a.img_url,a.unique_id,'',now(),a.property_area_num,a.description,a.longitude,a.latitude,'' \
    from auctionapp_auction as a, geo_areas as g, asset_type as t \
    where (a.asset_type='realestate' or a.asset_type='real estate') and a.transaction_type='commercial' and a.category_major='land' and \
    ( CONCAT(a.neighborhood,', ',trim((string_to_array(a.region,'-'))[1]),', Greece')=ANY(g.crawled_names) or CONCAT(a.neighborhood,', ',trim((string_to_array(a.region,'-'))[1]),', Greece')=g.name) and a.category_minor=ANY(t.synonyms) )on conflict do nothing;"

    cursor.execute(update_prop_land)

    update_prop_auction="INSERT into prop_auction (title,mainarea_id,secondarea_id,address,asset_type_id,img_url, \
    unique_id,status,updated_date,embadon,other,longitude,latitude) ( \
    SELECT a.title,g.city_id,g.id,a.address,13,a.img_url,a.unique_id,'',now(),a.property_area_num,a.description,g.longitude,g.latitude \
    from auctionapp_auction as a, geo_areas as g \
    where (a.asset_type='realestate' or a.asset_type='real estate' or a.asset_type='other') and a.transaction_type='auction' and \
    CONCAT(a.city,', Greece')=ANY(g.crawled_names) or a.city=ANY(g.crawled_names)\
    )on conflict do nothing;"

    cursor.execute(update_prop_auction)

    update_prop_comm = "INSERT into prop_commercial (title,mainarea_id,secondarea_id, address,asset_type_id,category_minor,img_url, \
    unique_id,status,updated_date,embadon,other,longitude,latitude,rooms,construction_year) ( SELECT \
    a.title,g.city_id,g.id,a.address,t.id,a.category_minor,a.img_url,a.unique_id,'',now(),a.property_area_num,a.description,a.longitude,a.latitude,a.property_rooms_num,a.construction_year \
    from auctionapp_auction as a, geo_areas as g, asset_type as t \
    where (a.asset_type='realestate' or a.asset_type='real estate') and a.transaction_type='commercial' and a.category_major='commercial' and \
    ( CONCAT(a.neighborhood,', ',trim((string_to_array(a.city,'-'))[1]),', Greece')=ANY(g.crawled_names) or CONCAT(a.neighborhood,', ',trim(a.city),', Greece')=ANY(g.crawled_names)) and \
    a.category_minor=ANY(t.synonyms) \
    )on conflict do nothing;"

    cursor.execute(update_prop_comm)

    update_prop_res = "INSERT into prop_residential (title,mainarea_id,secondarea_id,address,asset_type_id,category_minor,img_url, \
    unique_id,status,updated_date,embadon,other,longitude,latitude,bedrooms,construction_year) ( \
    SELECT a.title,g.city_id,g.id,a.address,t.id,a.category_minor,a.img_url,a.unique_id,'',now(),a.property_area_num,a.description,a.longitude,a.latitude,a.property_rooms_num,a.construction_year \
    from auctionapp_auction as a, geo_areas as g, asset_type as t \
    where (a.asset_type='realestate' or a.asset_type='real estate') and a.transaction_type='commercial' and (a.category_major='residential' or a.category_major='homes') and \
    ( CONCAT(a.neighborhood,', ',trim((string_to_array(a.city,'-'))[1]),', Greece')=ANY(g.crawled_names) or CONCAT(a.neighborhood,', ',trim(a.city),', Greece')=ANY(g.crawled_names)) and \
    a.category_minor=ANY(t.synonyms) \
    )on conflict do nothing;"

    cursor.execute(update_prop_res)

def delete_properties():
    cursor = init_connection()
    delete_query = "TRUNCATE TABLE asset CASCADE; \
    ALTER SEQUENCE asset_id_seq RESTART WITH 1; "

    cursor.execute(delete_query)

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def getGoogleMapsClient():
    api_keys = ['AIzaSyAceR3rS8GL-yCvtmZ2Yf_zn6U7NHtvKxA','AIzaSyD_WI3cBL-Qw4tuJU5f_J43G9jAmbXbMCE','AIzaSyD_4IyrrUGsjScz0bjwhwHcgt7a0iszh-w']

    for api_key in api_keys:
        try:
            gmaps = googlemaps.Client(key=api_key)
        except:
            continue

    return gmaps

def getPoiType(cursor,row_file):

    category_major = row_file['Category_Major'].strip()
    category_minor = row_file['Category_Minor'].strip()

    cursor.execute("SELECT * FROM poi_type WHERE (%s)=ANY(category_minor)" , (category_minor,))
    row = cursor.fetchall()
    if row:
        return "ok"

    else:
        cursor.execute("SELECT category_minor FROM poi_type WHERE category_major=(%s)" , (category_major,))

        found_area = cursor.fetchall()

        # if crawled area is different but area is already in database
        if found_area:
            found_minors = found_area[0][0]

            found_minors.append(category_minor)
            cursor.execute("UPDATE poi_type SET category_minor=(%s) WHERE category_major=(%s)" , (found_minors,category_major,))

        else:
            cursor.execute("INSERT INTO poi_type(category_major,category_minor) VALUES(%s,%s)", (category_major,[category_minor]))

            return "added"

def add_pois():
    countries = []
    regions = []
    cities = []
    areas = []

    gmaps = googlemaps.Client(key='AIzaSyAceR3rS8GL-yCvtmZ2Yf_zn6U7NHtvKxA')

    # gmaps = googlemaps.Client(key='AIzaSyD_WI3cBL-Qw4tuJU5f_J43G9jAmbXbMCE')
    # api_key1 = "AIzaSyAceR3rS8GL-yCvtmZ2Yf_zn6U7NHtvKxA"
    # api_key2 = 'AIzaSyD_4IyrrUGsjScz0bjwhwHcgt7a0iszh-w'
    # 'AIzaSyD_WI3cBL-Qw4tuJU5f_J43G9jAmbXbMCE'

    cursor = init_connection()

    cursor.execute("truncate poi CASCADE; ALTER SEQUENCE poi_id_seq RESTART WITH 1;truncate geo_address CASCADE; ALTER SEQUENCE geo_address_id_seq RESTART WITH 1;")


    df = pd.read_csv('/Users/konstantinosskianis/Documents/auctions/auctionapp_poi_v6.csv')

    df = df.replace(np.nan, '', regex=True)
    df['Postcode']=df['Postcode'].replace('', -1, regex=True)
    df['Postcode']=df['Postcode'].replace(' ', '',regex=True)
    df['Postcode']=df['Postcode'].replace('"', '',regex=True)
    df['Recommended']=df['Recommended'].replace('', 0, regex=True)
    df['Score']=df['Score'].replace('', -1, regex=True)
    df['On map']=df['On map'].replace('', -1, regex=True)
    df['Importance']=df['Importance'].replace('', 0, regex=True)
    df['ln']=df['ln'].replace('', -1, regex=True)
    df['lt']=df['lt'].replace('', -1, regex=True)

    for index, row_file in df.iterrows():

        # getPoiType(cursor,row_file)
        postcode = row_file['Postcode']
        address = row_file['Address']
        area = row_file['Area']
        if address and area:
            cursor.execute("SELECT * FROM geo_address WHERE name=%s" , (address,))

            # cursor.execute("SELECT * FROM poi WHERE full_title=(%s)" , (row_file['Full_title'],))

            row = cursor.fetchall()
            # if row:
            #     print "Poi already in database",

            if not row:

                # geocode_result = gmaps.geocode(address)
                #
                # print geocode_result
                #
                # if geocode_result:
                #     address_components = geocode_result[0]['address_components']
                #
                #     address = address_components[0]['long_name']
                #
                #     postcode = ""
                #     city = ""
                #     region = ""
                #     country = ""
                #
                #     for component in address_components:
                #         if 'postal_code' in component['types']:
                #             postcode = component['short_name'].replace(" ", "")
                #             break
                #
                #
                #     for component in address_components:
                #         if 'locality' in component ['types']:
                #             area = component['short_name']
                #             break
                #
                #
                #     for component in address_components:
                #         if 'administrative_area_level_3' in component['types']:
                #             region = component['long_name']
                #             break
                #
                #
                #     if city=="":
                #         # city = region
                #         # city = city_bef
                #         city = area
                #
                #     for component in address_components:
                #         if 'country' in component ['types']:
                #             country = component['long_name']
                #             break
                #
                #     latitude = geocode_result[0]['geometry']['location']['lat']
                #     longitude = geocode_result[0]['geometry']['location']['lng']
                #
                #

                # print row_file['Area']
                # print row_file['Region']
                search_str = row_file['Area']+", "+row_file['Region']+", Greece"

                cursor.execute("SELECT id FROM geo_areas WHERE name=(%s) or (%s)=ANY(crawled_names)" , (search_str,search_str,))

                row = cursor.fetchall()
                if row:
                    area_id = row[0][0]


                    # cursor.execute("INSERT into geo_address (name,latitude,longitude,area_id) VALUES (%s,%s,%s,%s) returning id;" , (address,latitude,longitude,area_id) )

                    latitude = row_file['lt']
                    longitude = row_file['ln']
                    postcode = row_file['Postcode']


                    cursor.execute("INSERT into geo_address (name,latitude,longitude,area_id) VALUES (%s,%s,%s,%s) returning id;" , (row_file['Address'],row_file['lt'],row_file['ln'],area_id) )


                    address_id = cursor.fetchall()[0][0]
                    # print address_id
                    # Look up an address with reverse geocoding
                    # reverse_geocode_result = gmaps.reverse_geocode((24.146362,41.151096))
                    # print row_file

                    cursor.execute("INSERT into poi (full_title,business,category_minor,category_major,website,email,phone,recommended,score,longitude,latitude,postcode,address_id,source,on_map,importance) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" , (row_file['Full_title'],row_file['Business'],row_file['Category_Minor'],row_file['Category_Major'],row_file['Website'],row_file['Email'],row_file['Phone'],row_file['Recommended'],row_file['Score'],longitude,latitude,postcode,address_id,row_file['Source'],row_file['On map'],row_file['Importance'],))

            # raw_input("enter")
