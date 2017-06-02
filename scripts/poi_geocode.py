# -*- coding: utf-8 -*-

import googlemaps
from datetime import datetime
import psycopg2
import pandas as pd
import math
import numpy as np

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

def main():
    countries = []
    regions = []
    cities = []
    areas = []

    # ALTER SEQUENCE geo_address_id_seq RESTART WITH 1;
    # ALTER SEQUENCE poi_id_seq RESTART WITH 1;

    gmaps = googlemaps.Client(key='AIzaSyAceR3rS8GL-yCvtmZ2Yf_zn6U7NHtvKxA')

    # gmaps = googlemaps.Client(key='AIzaSyD_WI3cBL-Qw4tuJU5f_J43G9jAmbXbMCE')
    # api_key1 = "AIzaSyAceR3rS8GL-yCvtmZ2Yf_zn6U7NHtvKxA"
    # api_key2 = 'AIzaSyD_4IyrrUGsjScz0bjwhwHcgt7a0iszh-w'
    # 'AIzaSyD_WI3cBL-Qw4tuJU5f_J43G9jAmbXbMCE'

    # INSERT into geo_regions (description,city_id)
    # (SELECT DISTINCT a.region,c.id FROM auctionapp_auction as a ,geo_cities as c
    #   where a.city=c.description);

    conn_string = "host='localhost' dbname='auctions' user='postgres' password='Dbt2bvrgef'"
    # print the connection string we will use to connect
    print "Connecting to database\n	->%s" % (conn_string)

    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)
    conn.autocommit = True

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()

    cursor.execute("truncate poi CASCADE; ALTER SEQUENCE poi_id_seq RESTART WITH 1;truncate geo_address CASCADE; ALTER SEQUENCE geo_address_id_seq RESTART WITH 1;")


    df = pd.read_csv('../../auctionapp_poi_v6.csv')
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


main()
