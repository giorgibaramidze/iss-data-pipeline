import json
from config import JSON_FILE_NAME, JSON_DIRECTORY_NAME, db_connection
from psycopg.rows import dict_row

import psycopg

with open(JSON_DIRECTORY_NAME + "/" + JSON_FILE_NAME, "r") as file:
    data = json.load(file)[-1]

insert_into = """
    INSERT INTO iss_data (
        latitude, longitude, altitude, velocity, visibility, 
        footprint, timestamp, daynum, solar_lat, solar_lon, units
    ) VALUES (
        %(latitude)s, %(longitude)s, %(altitude)s, %(velocity)s, %(visibility)s, 
        %(footprint)s, %(timestamp)s, %(daynum)s, %(solar_lat)s, %(solar_lon)s, %(units)s
    );
"""

select_from = """
    SELECT 
        latitude, longitude, altitude, velocity, visibility, 
        footprint, timestamp, daynum, solar_lat, solar_lon, units
    FROM iss_data
    ORDER BY timestamp DESC
    LIMIT 1;
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
        with open("sql/create_table.sql", "r") as sql:
            cur.execute(sql.read())

    @connection()
    def insert_into(self, cur):
        cur.execute(insert_into, data)

    @connection()
    def select(self, cur):
        result = cur.execute(select_from)
        return result.fetchone()


a = Database(db_connection)
print(a.select())
