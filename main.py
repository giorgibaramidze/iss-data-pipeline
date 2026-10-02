import time

from alembic import command
from alembic.config import Config

from clients import GeocoderClient, ISSAPIClient
from config import (
    db_connection,
    ISS_API,
    JSON_DIRECTORY_NAME,
    JSON_FILE_LOCATION,
    OPENCAGE_API_KEY,
    POLLING_INTERVAL,
)
from db.database import Database
from logger import logger
from services import ISSCollector
from storage import JSONStorage


def main():
    """Run the ISS tracking pipeline continuously."""

    logger.info("Starting ISS tracking pipeline execution...")

    try:
        db_action = Database(db_connection)
        db_action.create_database()

        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")

        storage = JSONStorage(JSON_DIRECTORY_NAME, JSON_FILE_LOCATION)
        storage.initialize()

        iss_client = ISSAPIClient(ISS_API)
        geocoder_client = GeocoderClient(OPENCAGE_API_KEY)
        collector = ISSCollector(iss_client, geocoder_client, storage)

    except Exception as e:
        logger.error(f"Pipeline initialization failed: {e}")
        return

    while True:
        try:
            iss_data, location = collector.collect_data()

            distance_km = db_action.fetch_traveled_distance(
                current_rec=iss_data
            )

            iss_id = db_action.insert_into_iss_data(
                current_rec=iss_data
            )

            db_action.insert_into_iss_enriched(
                iss_id=iss_id,
                location=location,
                distance_km=distance_km,
            )

            place_name = (
                location.get("city")
                or location.get("country")
                or location.get("body_of_water")
                or "Unknown Location"
            )

            velocity = iss_data.get("velocity")

            logger.info(
                f"SUMMARY: ISS Record #{iss_id} | "
                f"Location: {place_name} | "
                f"Distance since last reading: {distance_km:.2f} km | "
                f"Velocity: {velocity:.2f} km/h"
            )

        except Exception as e:
            logger.error(f"Pipeline execution step failed: {e}")

        time.sleep(POLLING_INTERVAL)


if __name__ == "__main__":
    main()