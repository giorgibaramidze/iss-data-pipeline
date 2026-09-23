from time import perf_counter
import requests
from opencage.geocoder import OpenCageGeocode
from storage import JSONStorage

from config import (
    JSON_DIRECTORY_NAME,
    OPENCAGE_API_KEY,
    ISS_API,
    JSON_FILE_LOCATION
)


class ISSAPIClient:
    def __init__(self, iss_api_key, opencage_api_key):
        self.iss_api_key = iss_api_key
        self.opencage_api_key = opencage_api_key

    def fetch_iss_data(self):
        response = requests.get(self.iss_api_key)
        return response.json()

    def iss_location(self, lat, lon):
        response = OpenCageGeocode(self.opencage_api_key)
        data = response.reverse_geocode(lat, lon)

        components = data[0]["components"]

        location = {
            "country": components.get("country"),
            "city": components.get("city"),
            "body_of_water": components.get("body_of_water"),
        }

        return location


            
class ISSCollector:

    def __init__(self, api_client, storage):
        self.api_client = api_client
        self.storage = storage


    def collect_data(self):
        iss_data = self.api_client.fetch_iss_data()

        location = self.api_client.iss_location(
            iss_data["latitude"],
            iss_data["longitude"]
        )
        self.storage.save_to_lake(iss_data)

        return {
            "iss_data": iss_data,
            "location": location
        }

if __name__ == "__main__":
    storage = JSONStorage(JSON_DIRECTORY_NAME, JSON_FILE_LOCATION)
    api_client = ISSAPIClient(ISS_API, OPENCAGE_API_KEY)
    collector = ISSCollector(api_client, storage)
    collector.collect_data()
