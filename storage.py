import json
import os

class JSONStorage:
    def __init__(self, json_directory_location, json_file_location):
        self.json_directory_location = json_directory_location
        self.json_file_location = json_file_location
    
        self._create_data_directory()
        self._create_json_file()
    
    def _create_data_directory(self):
        os.makedirs(self.json_directory_location, exist_ok=True)
        
    def _create_json_file(self):
        if not os.path.exists(self.json_file_location):
            with open(self.json_file_location, "w") as file:
                json.dump([], file)

    def _read_lake(self):
        with open(self.json_file_location, "r") as file:
            return json.load(file)

    def save_to_lake(self, new_data):
        data_lake = self._read_lake()
        data_lake.append(new_data) 
        with open(self.json_file_location, "w") as file:
            json.dump(data_lake, file, indent=4)