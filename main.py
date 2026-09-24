from database import Database
from storage import JSONStorage
from services import ISSCollector
from clients import ISSAPIClient, GeocoderClient

from config import (
    JSON_DIRECTORY_NAME,
    OPENCAGE_API_KEY,
    ISS_API,
    JSON_FILE_LOCATION,
    db_connection
)


db_action = Database(db_connection)
storage = JSONStorage(JSON_DIRECTORY_NAME, JSON_FILE_LOCATION)
print("step 1")
db_action.create_database()
print("step 2")
db_action.create_tables()
print("step 3")
if __name__ == "__main__":
    print("step 4")
    iss_client = ISSAPIClient(ISS_API)
    geocoder_client = GeocoderClient(OPENCAGE_API_KEY)
    collector = ISSCollector(iss_client, geocoder_client, storage)
    iss_data, location = collector.collect_data()
    result = db_action.fetch_traveled_distance(current_rec=iss_data)
    iss_id = db_action.insert_into_iss_data(current_rec=iss_data)
    db_action.insert_into_iss_enriched(iss_id=iss_id, location=location, distance_km=result)
    
    print(db_action.select_highest_velocity())
    print(db_action.count_visibility())