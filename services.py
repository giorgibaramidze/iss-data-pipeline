class ISSCollector:

    def __init__(self, iss_client, geocoder_client, storage):
        self._iss_client = iss_client
        self._geocoder_client = geocoder_client
        self._storage = storage

    def collect_data(self):
        iss_data = self.api_client.fetch_iss_data()
        lat = iss_data.get("latitude")
        lon = iss_data.get("longitude")

        location = self.api_client.iss_location(lat, lon)
        self.storage.save_to_lake(iss_data)

        return iss_data, location