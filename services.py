class ISSCollector:

    def __init__(self, iss_client, geocoder_client, storage):
        self._iss_client = iss_client
        self._geocoder_client = geocoder_client
        self._storage = storage

    def collect_data(self):
        iss_data = self._iss_client.get_iss_data()
        lat = iss_data.get("latitude")
        lon = iss_data.get("longitude")

        location = self._geocoder_client.get_iss_location(lat, lon)
        self._storage.save_to_lake(iss_data)

        return iss_data, location