import json
import os

import requests
from opencage.geocoder import OpenCageGeocode

from config import (
    JSON_DIRECTORY_NAME,
    JSON_FILE_NAME,
    OPENCAGE_API_KEY,
    ISS_API
)


class ISSAPIClient:

    def fetch_iss_data(self):
        response = requests.get(ISS_API)
        response.raise_for_status()

        return response.json()

    def iss_location(self, lat, lon):
        response = OpenCageGeocode(OPENCAGE_API_KEY)
        data = response.reverse_geocode(lat, lon)

        components = data[0]["components"]

        location = {
            "country": components.get("country"),
            "city": components.get("city"),
            "body_of_water": components.get("body_of_water"),
        }

        return location


class ISSCollector:

    JSON_FILE_LOCATION = os.path.join(
        JSON_DIRECTORY_NAME,
        JSON_FILE_NAME
    )

    def __init__(self, api_client):
        self.api_client = api_client

        self._create_data_directory()
        self._create_json_file()

    def _create_data_directory(self):
        os.makedirs(JSON_DIRECTORY_NAME, exist_ok=True)

    def _create_json_file(self):
        if not os.path.exists(self.JSON_FILE_LOCATION):
            with open(self.JSON_FILE_LOCATION, "w") as file:
                json.dump([], file)

    def _read_lake(self):
        with open(self.JSON_FILE_LOCATION, "r") as file:
            return json.load(file)

    def _save_to_lake(self, new_data):
        data_lake = self._read_lake()
        data_lake.append(new_data) 
        with open(self.JSON_FILE_LOCATION, "w") as file:
            json.dump(data_lake, file, indent=4)

    def collect_data(self):
        iss_data = self.api_client.fetch_iss_data()

        location = self.api_client.iss_location(
            iss_data["latitude"],
            iss_data["longitude"]
        )
        self._save_to_lake(iss_data)

        return {
            "iss_data": iss_data,
            "location": location
        }


if __name__ == "__main__":
    api_client = ISSAPIClient()
    collector = ISSCollector(api_client)
    print(collector.collect_data())
