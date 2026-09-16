import json
import requests
import os
from config import JSON_DIRECTORY_NAME, JSON_FILE_NAME

url = "https://api.wheretheiss.at/v1/satellites/25544"

def get_current_position():
    response = requests.get(url)
    data = response.json()

    return data



class JSONStorage:
    JSON_FILE_LOCATION = JSON_DIRECTORY_NAME + "/" + JSON_FILE_NAME

    def __init__(self, IIS_Position):
        self.IIS_Position = IIS_Position

    def _read(self):
        if not os.path.exists(self.JSON_FILE_LOCATION):
            os.mkdir(JSON_DIRECTORY_NAME)
            return []

        with open(self.JSON_FILE_LOCATION, "r") as file:
            data = json.load(file)

        return data


    def write(self):
        result = self._read()
        result.append(self.IIS_Position)
        with open(self.JSON_FILE_LOCATION, "w") as file:
            json.dump(result, file, indent=4)

if __name__ == "__main__":
    position = get_current_position()
    write_data = JSONStorage(position)
    write_data.write()
