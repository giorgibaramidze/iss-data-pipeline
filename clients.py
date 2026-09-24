import requests
from opencage.geocoder import OpenCageGeocode

class ISSAPIClient:
    def __init__(self, iss_api_url):
        self.iss_api_url = iss_api_url

    def get_iss_data(self):
        response = requests.get(self.iss_api_url)
        response.raise_for_status()
        return response.json()


class GeocoderClient:
    def __init__(self, api_key):
        self.geocoder = OpenCageGeocode(api_key)


    def get_iss_location(self, lat, lon):
        data = self.geocoder.reverse_geocode(lat, lon)
    
        if not data:
            return {
                "country": None,
                "city": None,
                "body_of_water": None,                }
    
        components = data[0].get("components", {})
    
        location = {
            "country": components.get("country"),
            "city": components.get("city"),
            "body_of_water": components.get("body_of_water"),
        }
    
        return location