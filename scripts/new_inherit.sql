-- drop schema public cascade;
-- create schema public;

CREATE TABLE geo_countries (
  id serial PRIMARY KEY,
  name varchar(250)
);

CREATE TABLE geo_regions (
  id serial PRIMARY KEY,
  name varchar(250),
  country_id integer REFERENCES geo_countries (id),
  other_names character varying(250)[]
);

CREATE TABLE geo_cities (
  id serial PRIMARY KEY,
  name varchar(250),
  region_id integer REFERENCES geo_regions (id),
  other_names character varying(250)[]
);

CREATE TABLE geo_areas (
  id serial PRIMARY KEY,
  name varchar(250),
  crawled_names varchar(250)[],
  postcode varchar(250),
  longitude float,
  latitude float,
  city_id integer REFERENCES geo_cities (id)
);

CREATE TABLE sources (
  id SERIAL PRIMARY KEY,
  source_text text,
  last_crawled date,
  source_type
);

-------------------- ASSET ----------------------------

CREATE TABLE asset (
  id SERIAL PRIMARY KEY,
  title varchar(250),
  mainarea_id integer REFERENCES geo_cities (id),
  secondarea_id integer REFERENCES geo_areas (id),
  percentage varchar(150) DEFAULT NULL,
  address varchar(150) DEFAULT NULL,
  img_url varchar(250),
  unique_id varchar(250),
  performance_category varchar(250),
  suggest_price float,
  suggest_income float,
  category_major varchar(250),
  status varchar(20),
  updated_date date,
  profit_loss_income float,
  imgs varchar(250)[],
  features varchar(200)[],
  geo text,
  unique (title, unique_id)
);

CREATE TABLE asset_property (
  embadon float,
  price float,
  other text,
  longitude float,
  latitude float,
  asset_type integer REFERENCES asset_property_type (id),
  unique (title,asset_type, unique_id)
) INHERITS (asset);

CREATE TABLE asset_car (
  car_kms_num integer,
  car_cc_num integer,
  fuel_type varchar(150),
  first_hand boolean,
  other text,
  unique (title,unique_id)
) INHERITS (asset);

CREATE TABLE prop_earth (
  inmap varchar(50) DEFAULT NULL,
  size float,
  unique (title,unique_id)
) INHERITS (asset_property);

CREATE TABLE prop_residential (
  bedrooms varchar(100),
  construction_year varchar(250),
  unique (title,asset_type, unique_id)
) INHERITS (asset_property);

CREATE TABLE prop_commercial (
  rooms integer,
  construction_year varchar(250),
  unique (title,asset_type, unique_id)
) INHERITS (asset_property);

CREATE TABLE prop_auction (
  UNIQUE (title,unique_id)
) INHERITS (asset_property);


-------------------- END OF ASSET ----------------------------

CREATE TABLE cooperator (
  id SERIAL PRIMARY KEY,
  contact_legal_name varchar(250),
  contact_name varchar(250),
  contact_phone varchar(250),
  contact_mobile varchar(250),
  contact_email varchar(250),
  contact_website varchar(250),
  coo_type integer DEFAULT NULL
);

CREATE TABLE search_info (
  id serial PRIMARY KEY,
  imported_date date,
  number_of_imports integer,
  unique(imported_date)
);


CREATE TABLE transaction(
  id serial PRIMARY KEY,
  search_id integer REFERENCES search_info (id),
  asset_id integer REFERENCES asset (id),
  name varchar(100) NOT NULL DEFAULT '',
  title varchar(250),
  url varchar(250),
  contact_legal_id integer REFERENCES cooperator (id),
  contact_website varchar(250),
  description varchar(250) NOT NULL DEFAULT '',
  source_id integer REFERENCES sources (id)
);

CREATE TABLE tran_auction (
  starting_price float,
  on_site_date date
) INHERITS (transaction);

CREATE TABLE tran_commercial (
  on_site_date date,
  selling_price float
) INHERITS (transaction);



CREATE TABLE asset_property_type (
  id serial PRIMARY KEY,
  description varchar(150) DEFAULT NULL,
  category_major varchar(150) DEFAULT NULL,
  synonyms varchar(150)[] DEFAULT NULL
)

CREATE TABLE poi (
  id serial PRIMARY KEY,
  description varchar(150) DEFAULT NULL,
  description1 varchar(150) DEFAULT NULL,
  type varchar(150) DEFAULT NULL,
  place varchar(150) DEFAULT NULL,
  area varchar(150) DEFAULT NULL,
  latitude float,
  longitude float,
  address varchar(150) DEFAULT NULL,
);


ALTER TABLE prop_commercial
ADD UNIQUE (title, secondarea, asset_type, embadon, unique_id)

ALTER TABLE asset_property
   ADD CONSTRAINT fk_asset_type
   FOREIGN KEY (asset_type)
   REFERENCES asset_property_type(id);
