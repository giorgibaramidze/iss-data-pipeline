from psycopg.rows import dict_row
from queries import (
    CREATE_DATABASE,
    CREATE_TABLE_ISS_DATA,
    CREATE_TABLE_ISS_ENRICHED,
    INSERT_INTO_ISS_DATA,
    INSERT_ISS_ENRICHED,
    SELECT_HIGHEST_VELOCITY,
    SELECT_LAST_TIMESTAMP,
    SELECT_VISIBILITY_COUNT
)
import psycopg


def connection(autocommit=False):
    def decorator(fn):
        def wrapper(self, *args, **kwargs):
            try:
                with psycopg.connect(**self.config, row_factory=dict_row, autocommit=autocommit) as conn:
                    with conn.cursor() as cur:
                        return fn(self, cur, *args, **kwargs)
            except Exception as e:
                raise e
        return wrapper
    return decorator


class Database:
    def __init__(self, config):
        self.config = config

    #create tables and databases
    @connection(autocommit=True)
    def create_database(self, cur):
        try:
            cur.execute(CREATE_DATABASE)
        except psycopg.errors.DuplicateDatabase as e:
            print(e)

    @connection()
    def create_tables(self, cur):
        cur.execute(CREATE_TABLE_ISS_DATA)
        cur.execute(CREATE_TABLE_ISS_ENRICHED)


    #perform insert data
    @connection()
    def insert_into_iss_data(self, cur, current_rec):
        result = cur.execute(INSERT_INTO_ISS_DATA, current_rec)
        return result.fetchone()["id"]

    @connection()
    def insert_into_iss_enriched(self, cur, iss_id, location, distance_km):
        cur.execute(INSERT_ISS_ENRICHED, {"iss_data_id": iss_id, "distance_km":distance_km,  **location})


    #perform select actions
    @connection()
    def select_highest_velocity(self, cur):
        result = cur.execute(SELECT_HIGHEST_VELOCITY)
        return result.fetchone()

    @connection()
    def count_visibility(self, cur):
        result = cur.execute(SELECT_VISIBILITY_COUNT)
        return result.fetchall()


    @connection()
    def fetch_traveled_distance(self, cur, current_rec):
        timestamp = cur.execute(SELECT_LAST_TIMESTAMP)
        timestamp_dict = timestamp.fetchone()

        if timestamp_dict is None:
            return 0

        diff_in_seccond = current_rec.get("timestamp") - timestamp_dict.get("timestamp")
        distance_km = diff_in_seccond * current_rec.get("velocity") / 3600
        return distance_km