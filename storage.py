import json
import os

class JSONStorage:
    """Handles reading and writing data to a JSON file."""
    def __init__(self, json_directory_location, json_file_location):
        self.json_directory_location = json_directory_location
        self.json_file_location = json_file_location
    
    def initialize(self):
        """Create the storage directory and JSON file if they do not exist."""
        self._create_data_directory()
        self._create_json_file()
    
    def _create_data_directory(self):
        os.makedirs(self.json_directory_location, exist_ok=True)
        
    def _create_json_file(self):
        if not os.path.exists(self.json_file_location):
            with open(self.json_file_location, "w") as file:
                json.dump([], file)

    def _read_from_json(self):
        with open(self.json_file_location, "r") as file:
            return json.load(file)

    def save_to_json(self, new_data):
        """Append a new record to the JSON file."""
        data = self._read_from_json()
        data.append(new_data) 
        with open(self.json_file_location, "w") as file:
            json.dump(data, file, indent=4)