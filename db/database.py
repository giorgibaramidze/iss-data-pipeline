from functools import wraps

import psycopg
from psycopg.rows import dict_row

from config import DB_NAME
from logger import logger
from db.queries import (
    CREATE_DATABASE,
    INSERT_INTO_ISS_DATA,
    INSERT_ISS_ENRICHED,
    SELECT_HIGHEST_VELOCITY,
    SELECT_LAST_TIMESTAMP,
    SELECT_VISIBILITY_COUNT,
)


SECONDS_PER_HOUR = 3600


def connection(autocommit=False):
    """Create a decorator that manages a database connection for a method."""

    def decorator(fn):
        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            try:
                connection_config = self.config

                if fn.__name__ == "create_database":
                    connection_config = {
                        **self.config,
                        "dbname": "postgres",
                    }
                with psycopg.connect(
                    **connection_config,
                    row_factory=dict_row,
                    autocommit=autocommit,
                ) as conn:
                    with conn.cursor() as cur:
                        return fn(self, cur, *args, **kwargs)

            except Exception:
                logger.exception(f"Database error in {fn.__name__}")
                raise

        return wrapper

    return decorator


class Database:
    """Provides database operations for the ISS tracking pipeline."""

    def __init__(self, config):
        self.config = config

    @connection(autocommit=True)
    def create_database(self, cur):
        """Create the database if it does not already exist."""
        try:
            cur.execute(CREATE_DATABASE)
            logger.info(f"Database {DB_NAME} created successfully.")
        except psycopg.errors.DuplicateDatabase:
            logger.info(f"Database {DB_NAME} already exists.")


    @connection()
    def insert_into_iss_data(self, cur, current_rec):
        """Insert an ISS record and return its database ID."""
        result = cur.execute(INSERT_INTO_ISS_DATA, current_rec)
        return result.fetchone()["id"]

    @connection()
    def insert_into_iss_enriched(self, cur, iss_id, location, distance_km):
        """Insert location and distance data related to an ISS record."""
        cur.execute(
            INSERT_ISS_ENRICHED,
            {
                "iss_data_id": iss_id,
                "distance_km": distance_km,
                **location,
            },
        )

    @connection()
    def select_highest_velocity(self, cur):
        """Return the ISS record with the highest velocity."""
        result = cur.execute(SELECT_HIGHEST_VELOCITY)
        return result.fetchone()

    @connection()
    def count_visibility(self, cur):
        """Return visibility counts from the ISS data."""
        result = cur.execute(SELECT_VISIBILITY_COUNT)
        return result.fetchall()

    @connection()
    def fetch_traveled_distance(self, cur, current_rec):
        """Calculate the distance traveled since the previous ISS record."""
        timestamp = cur.execute(SELECT_LAST_TIMESTAMP)
        timestamp_dict = timestamp.fetchone()

        if timestamp_dict is None:
            return 0

        diff_in_seconds = (
            current_rec.get("timestamp")
            - timestamp_dict.get("timestamp")
        )

        distance_km = (
            diff_in_seconds
            * current_rec.get("velocity")
            / SECONDS_PER_HOUR
        )

        return distance_km