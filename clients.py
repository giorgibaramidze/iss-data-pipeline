import requests
from opencage.geocoder import OpenCageGeocode


class ISSAPIClient:
    """Client for fetching ISS data from the external API."""

    def __init__(self, iss_api_url):
        self._iss_api_url = iss_api_url

    def get_iss_data(self):
        """Fetch and return the latest ISS data."""
        response = requests.get(self._iss_api_url, timeout=10)
        response.raise_for_status()
        return response.json()


class GeocoderClient:
    """Client for converting coordinates into location information."""

    def __init__(self, api_key):
        self._geocoder = OpenCageGeocode(api_key)

    def get_iss_location(self, lat, lon):
        """Return location information for the given coordinates."""
        data = self._geocoder.reverse_geocode(lat, lon)

        if not data:
            return {
                "country": None,
                "city": None,
                "body_of_water": None,
            }

        components = data[0].get("components", {})

        location = {
            "country": components.get("country"),
            "city": components.get("city"),
            "body_of_water": components.get("body_of_water"),
        }

        return location