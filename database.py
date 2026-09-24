import json
from config import JSON_FILE_NAME, JSON_DIRECTORY_NAME, db_connection
from psycopg.rows import dict_row
import time
from storage import JSONStorage
from main import ISSAPIClient, ISSCollector

from config import (
    JSON_DIRECTORY_NAME,
    OPENCAGE_API_KEY,
    ISS_API,
    JSON_FILE_LOCATION
)

import psycopg

create_table = """
    CREATE TABLE IF NOT EXISTS iss_data (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	iss_id DECIMAL(10, 2) NOT NULL,
	latitude DECIMAL(10, 2) NOT NULL,
	longitude DECIMAL(10, 2) NOT NULL,
	altitude DECIMAL(10, 2) NOT NULL,
	velocity DECIMAL(10, 2) NOT NULL,
	visibility VARCHAR(32) NOT NULL,
	footprint DECIMAL(10, 2) NOT NULL,
	timestamp BIGINT NOT NULL,
	daynum DECIMAL(10, 2) NOT NULL,
	solar_lat DECIMAL(10, 2) NOT NULL,
	solar_lon DECIMAL(10, 2) NOT NULL,
	units VARCHAR(12) NOT NULL
);

"""


insert_into_iss_data = """
    INSERT INTO iss_data (
        iss_id, latitude, longitude, altitude, velocity, visibility, 
        footprint, timestamp, daynum, solar_lat, solar_lon, units
    ) VALUES (
        %(id)s, %(latitude)s, %(longitude)s, %(altitude)s, %(velocity)s, %(visibility)s, 
        %(footprint)s, %(timestamp)s, %(daynum)s, %(solar_lat)s, %(solar_lon)s, %(units)s
    ) RETURNING id;
"""


create_iss_enriched = """
    CREATE TABLE IF NOT EXISTS iss_enriched (
        id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        iss_data_id BIGINT NOT NULL,
        distance_km DECIMAL(12, 2) NOT NULL,
        country VARCHAR(128),
        city VARCHAR(128),
        body_of_water VARCHAR(128),

        FOREIGN KEY (iss_data_id)
            REFERENCES iss_data(id)
    );
"""


insert_iss_enriched = """
    INSERT INTO iss_enriched (
        iss_data_id, distance_km, country, city, body_of_water
    ) VALUES (
        %(iss_data_id)s, %(distance_km)s, %(country)s, %(city)s, %(body_of_water)s
)
"""
def connection(autocommit=False):
    def decorator(fn):
        def wrapper(self, *args, **kwargs):
            try:
                with psycopg.connect(**self.config, row_factory=dict_row) as conn:
                    conn.autocommit = autocommit
                    with conn.cursor() as cur:
                        return fn(self, cur, *args, **kwargs)
                    
            except Exception as e:
                print(e)
        return wrapper
    return decorator

class Database:
    def __init__(self, config):
        self.config = config


    @connection(autocommit=True)
    def create_database(self, cur):
        cur.execute("CREATE DATABASE wheretheiss;")

    @connection()
    def create_table(self, cur):
            cur.execute(create_table)

    @connection()
    def insert_into_iss_data(self, cur, current_rec):
        result = cur.execute(insert_into_iss_data, current_rec)
        return result.fetchone()["id"]


    @connection()
    def select_highest_velocity(self, cur):
        result = cur.execute("SELECT MAX(velocity) highest_velocity FROM iss_data")
        return result.fetchone()

    @connection()
    def count_visibility(self, cur):
        result = cur.execute("SELECT visibility,  COUNT(*) FROM iss_data GROUP BY visibility")
        return result.fetchall()


    @connection()
    def fetch_traveled_distance(self, cur, current_rec):
        timestamp = cur.execute("SELECT timestamp from iss_data order by timestamp desc limit 1")
        timestamp_dict = timestamp.fetchone()
        if timestamp_dict is None:
            return None
        diff_in_seccond = current_rec.get("timestamp") - timestamp_dict.get("timestamp")
        distance_km = diff_in_seccond * current_rec.get("velocity") / 3600
        return distance_km

    @connection()
    def insert_into_iss_enriched(self, cur, iss_id, location, distance_km):
        cur.execute(insert_iss_enriched, {"iss_data_id": iss_id, "distance_km":distance_km,  **location})
        



db_action = Database(db_connection)
storage = JSONStorage(JSON_DIRECTORY_NAME, JSON_FILE_LOCATION)
db_action.create_database()
db_action.create_table()
if __name__ == "__main__":
    api_client = ISSAPIClient(ISS_API, OPENCAGE_API_KEY)
    collector = ISSCollector(api_client, storage)
    iss_data, location = collector.collect_data()
    result = db_action.fetch_traveled_distance(current_rec=iss_data)
    # print("waiting next operation")
    iss_id = db_action.insert_into_iss_data(current_rec=iss_data)
    db_action.insert_into_iss_enriched(iss_id=iss_id, location=location, distance_km=result)
    
    print(db_action.select_highest_velocity())
    print(db_action.count_visibility())
    
        