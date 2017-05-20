# -*- coding: utf-8 -*-

import googlemaps
from datetime import datetime
import psycopg2

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

def main():
    countries = []
    regions = []
    cities = []
    areas = []

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

    # ## ERASE ALL AREAS
    # cursor.execute("truncate geo_areas CASCADE; ALTER SEQUENCE geo_areas_id_seq RESTART WITH 1;truncate geo_cities CASCADE; ALTER SEQUENCE geo_cities_id_seq RESTART WITH 1;truncate geo_regions CASCADE;ALTER SEQUENCE geo_regions_id_seq RESTART WITH 1;truncate geo_countries CASCADE;ALTER SEQUENCE geo_countries_id_seq RESTART WITH 1;")

    par="auction"

    # GENERATE CITIES
    if par=="commercial":
        cursor.execute("SELECT city,region,neighborhood FROM auctionapp_auction")
    else:
        cursor.execute("SELECT region,neighborhood,city FROM auctionapp_auction WHERE region IS NULL and neighborhood IS NULL")

    ## retrieve the records from the database
    records = cursor.fetchall()

    # cursor.execute("select neighborhood from auctionapp_auction where neighborhood='Ano Patisia'")
    # found_area = cursor.fetchall()
    # print found_area
    # raw_input("enter")
    #
    # # area = 'Ilisia'
    # cursor.execute("SELECT crawled_names FROM geo_areas WHERE name=(%s)" , ("ΑΝΩ ΠΑΤΗΣΙΑ",))
    # found_area = cursor.fetchall()
    # crawled_names = found_area[0][0]
    # print crawled_names
    # # # crawled_names.append("'some'")
    # # # cursor.execute("UPDATE geo_areas SET crawled_names=(%s) WHERE name=(%s)" , (lst2pgarr(crawled_names),area,))
    # raw_input("enter")

    # geocode_result = gmaps.geocode('Pefka, Thessaloniki, Greece')
    # geocode_result = gmaps.geocode("Peristeri, Athens, Greece")
    # geocode_result = gmaps.geocode("spata, athens, greece")

    # print geocode_result
    # area = geocode_result[0]['address_components'][0]['long_name']
    #
    # print RepresentsInt( area )
    # # print not set(['neighborhood','locality','political']).isdisjoint(geocode_result[0]['address_components'][0]['types'])
    # print geocode_result[0]['types']
    # print set(['neighborhood','locality','political']).isdisjoint(geocode_result[0]['types'])
    # raw_input("enter")
    #
    # print geocode_result[0]['formatted_address']+" "+str(geocode_result[0]['address_components'])

    crawled_areas = []
    countries = []
    regions = []
    cities = []

    not_found_counter = 0

    for record in records:

        if record[2] is not None:

            # Geocoding an address
            # neigh = record[0]['neighborhood']

            s_un = record[2] #.decode("utf-8")
            crawled_names = []

            if "-" in s_un:

                s_cl = s_un.split("-")
                s_yo = s_cl[0].strip()

            else:
                s_yo = s_un.strip()


            # city_bef = record[0].split("-")[0].strip()

            if s_yo=="Kentro" or s_yo=="Center" or s_yo=="Historic Center" :
                s_yo = record[0].split("-")[0].strip()

            # s_yo = s_yo.decode("utf-8")
            s_without = s_yo

            if par=="commercial":
                s = s_yo+", "+record[0].split("-")[0].strip()+", Greece"
            else:
                s = s_yo
            # s = s.decode("utf-8")

            s_prev = s
            # if s in crawled_areas or s in areas:
            #     cursor.execute("SELECT description FROM geo_areas WHERE crawled_descr='"+s+"'")
            #     row = cursor.fetchall()

            ##check if area is already in database
            cursor.execute("SELECT * FROM geo_areas WHERE (%s)=ANY(crawled_names) or %s=name" , (s,s,))
            # retrieve the records from the database
            crawled_area = cursor.fetchall()

            # print "crawled_area:"+str(crawled_area)
            # raw_input("enter")

            if crawled_area:

                print s+": area existing in database"

            else:

                # geocode_result = gmaps.geocode(s)

                if "Suburbs" in s or "Com." in s or "Rest Of" in s:
                    # s_without = s_cl[1].strip()
                    s = s.replace("Suburbs","").strip()
                    s = s.replace("Com.","").strip()
                    s = s.replace("Rest Of","").strip()

                geocode_result = gmaps.geocode(s)

                if not geocode_result: ## for example make Saronida, Athens, Greece->Saronida, Greece
                    s = s_yo+", Greece"

                try:
                    address_components = geocode_result[0]['address_components']

                    # for component in address_components:
                    #     if 'administrative_area_level_3' in geocode_result[0]['types']:
                    #         city_bool=True

                    #point_of_interest','establishment'

                    if set(['neighborhood','locality','political','point_of_interest','establishment']).isdisjoint(geocode_result[0]['types']):
                        s = s_yo+", Greece"
                        geocode_result = gmaps.geocode(s)
                        address_components = geocode_result[0]['address_components']

                except:
                    not_found_counter += 1
                    # raw_input("enter")
                    continue

                ##check if area is already in database

                # s.replace("\"","")
                # s.replace("\'","")

                cursor.execute("SELECT * FROM geo_areas WHERE (%s)=ANY(crawled_names) or %s=name" , (s,s,))
                # retrieve the records from the database
                crawled_area = cursor.fetchall()

                # recheck
                if crawled_area:

                    print s+": area existing in database in 2nd check"

                else:

                    area = address_components[0]['long_name']
                    if RepresentsInt( area.replace(" ","") ):
                        area = s_yo

                    postcode = ""
                    city = ""
                    region = ""
                    country = ""

                    for component in address_components:
                        if 'postal_code' in component['types']:
                            postcode = component['short_name'].replace(" ", "")
                            break


                    for component in address_components:
                        if 'locality' in component ['types']:
                            city = component['short_name']
                            break


                    for component in address_components:
                        if 'administrative_area_level_3' in component['types']:
                            region = component['long_name']
                            break


                    if city=="":
                        # city = region
                        # city = city_bef
                        city = area


                    for component in address_components:
                        if 'country' in component ['types']:
                            country = component['long_name']
                            break

                    latitude = geocode_result[0]['geometry']['location']['lat']
                    longitude = geocode_result[0]['geometry']['location']['lng']


                    try:
                        cursor.execute("SELECT crawled_names FROM geo_areas WHERE name=(%s)" , (area+", "+city+", "+country,))
                    except:
                        area = area.decode("utf-8")
                        city = city.decode("utf-8")
                        country = country.decode("utf-8")
                        cursor.execute("SELECT crawled_names FROM geo_areas WHERE name=(%s)" , (area+", "+city+", "+country,))
                        pass

                    found_area = cursor.fetchall()

                    # if crawled area is different but area is already in database
                    if found_area:
                        crawled_names = found_area[0][0]
                        if s_prev not in crawled_names:
                            print "found existing crawled_name"
                            # s_array = found_area[0][0].replace("}","]")
                            # s_array = s_array.replace("{","[")
                            # print s_array

                            crawled_names.append(s_prev)
                            cursor.execute("UPDATE geo_areas SET crawled_names=(%s) WHERE name=(%s)" , (crawled_names,area+", "+city+", "+country,))

                    else:
                        crawled_names.append(s_prev)

                        cursor.execute("SELECT name FROM geo_countries")

                        countries = [row_co[0] for row_co in cursor]

                        if country not in countries:
                            countries.append(country)
                            cursor.execute("INSERT into geo_countries (name) VALUES (%s)" , (country,))

                        cursor.execute("SELECT id FROM geo_countries WHERE name=%s" , (country,))

                        row = cursor.fetchall()
                        country_id = row[0]

                        # if region not in regions:
                        #     regions.append(region)
                        #     cursor.execute("INSERT into geo_regions (name,country_id) VALUES (%s,%s)" , (region,country_id))

                        ## check if region is in synonyms
                        cursor.execute("SELECT id,name,other_names FROM geo_regions WHERE name=(%s) or (%s)=ANY(other_names)" , (region,region,))
                        row = cursor.fetchall()

                        ## THIS IS FOR REGIONS
                        if row:
                            region_id = row[0][0]
                            region = row[0][1]
                            other_names = row[0][2]
                        else:
                            region_prev = region
                            geocode_result = gmaps.geocode(region+", Greece")
                            address_components = geocode_result[0]['address_components']
                            region = address_components[0]['long_name']

                            ## double check
                            cursor.execute("SELECT id,name,other_names FROM geo_regions WHERE name=(%s) or (%s)=ANY(other_names)" , (region,region,))
                            row = cursor.fetchall()
                            # if city not in cities:
                            if row:
                                region_id = row[0][0]
                                region = row[0][1]
                                other_names = row[0][2]
                                other_names.append(region_prev)
                                cursor.execute("UPDATE geo_regions SET other_names=(%s) WHERE name=(%s)" , (other_names,region,))

                            else:
                                other_names = []
                                other_names.append(region_prev)
                                cursor.execute("INSERT into geo_regions (name,country_id,other_names) VALUES (%s,%s,%s)" , (region,country_id,other_names))

                        cursor.execute("SELECT id FROM geo_regions WHERE name=%s" , (region,))

                        row = cursor.fetchall()
                        region_id = row[0]


                        ## THIS IS FOR CITIES

                        ## check if city is in synonyms
                        cursor.execute("SELECT id,name,other_names FROM geo_cities WHERE name=(%s) or (%s)=ANY(other_names)" , (city,city,))
                        row = cursor.fetchall()

                        # if city not in cities:
                        if row:
                            # cities.append(city)
                            city_id = row[0][0]
                            city = row[0][1]
                            other_names = row[0][2]
                        else:
                            city_prev = city
                            geocode_result = gmaps.geocode(city+", Greece")
                            address_components = geocode_result[0]['address_components']
                            city = address_components[0]['long_name']

                            ## double check
                            cursor.execute("SELECT id,name,other_names FROM geo_cities WHERE name=(%s) or (%s)=ANY(other_names)" , (city,city,))
                            row = cursor.fetchall()
                            # if city not in cities:
                            if row:
                                city_id = row[0][0]
                                city = row[0][1]
                                other_names = row[0][2]
                                other_names.append(city_prev)
                                cursor.execute("UPDATE geo_cities SET other_names=(%s) WHERE name=(%s)" , (other_names,city,))

                            else:
                                other_names = []
                                other_names.append(city_prev)
                                cursor.execute("INSERT into geo_cities (name,region_id,other_names) VALUES (%s,%s,%s)" , (city,region_id,other_names))

                        cursor.execute("SELECT id FROM geo_cities WHERE name=%s" , (city,))

                        row = cursor.fetchall()
                        city_id = row[0]

                        # execute our Query
                        cursor.execute("INSERT into geo_areas (name,crawled_names,postcode,latitude,longitude,city_id) VALUES (%s,%s,%s,%s,%s,%s)" , (area+", "+city+", "+country,crawled_names,postcode,latitude,longitude,city_id))

                        crawled_areas.append(s)


                # areas.append(area)

                # raw_input("enter")

    print "Not found:"+str(not_found_counter)

main()
