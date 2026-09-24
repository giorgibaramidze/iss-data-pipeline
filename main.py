from database import Database
from storage import JSONStorage
from services import ISSCollector
from clients import ISSAPIClient, GeocoderClient
from logger import logger
from config import (
    JSON_DIRECTORY_NAME,
    OPENCAGE_API_KEY,
    ISS_API,
    JSON_FILE_LOCATION,
    db_connection
)


def main():
    logger.info("Starting ISS tracking pipeline execution...")
    try:
        db_action = Database(db_connection)
        db_action.create_database()
        db_action.create_tables()

        storage = JSONStorage(JSON_DIRECTORY_NAME, JSON_FILE_LOCATION)
        iss_client = ISSAPIClient(ISS_API)
        geocoder_client = GeocoderClient(OPENCAGE_API_KEY)
        collector = ISSCollector(iss_client, geocoder_client, storage)

        iss_data, location = collector.collect_data()

        distance_km = db_action.fetch_traveled_distance(current_rec=iss_data)
        iss_id = db_action.insert_into_iss_data(current_rec=iss_data)
        db_action.insert_into_iss_enriched(
            iss_id=iss_id, location=location, distance_km=distance_km
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
        logger.error(f"Pipeline execution failed: {e}")


if __name__ == "__main__":
    main()