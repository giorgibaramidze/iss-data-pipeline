from copy import deepcopy

from dotenv import dotenv_values
import os

config = dotenv_values()
OPENCAGE_API_KEY=config["OPENCAGE_API_KEY"]

DB_HOST=config["DB_HOST"]
DB_NAME=config["DB_NAME"]
DB_USER=config["DB_USER"]
DB_PASSWORD=config["DB_PASSWORD"]
DB_PORT=config["DB_PORT"]
OPENCAGE_API_KEY=config["OPENCAGE_API_KEY"]
ISS_API=config["ISS_API"]
JSON_FILE_NAME=config.get("JSON_FILE_NAME", "JSONData.json")
JSON_DIRECTORY_NAME=config.get("JSON_DIRECTORY_NAME", "storage/")
db_connection = dict(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)
JSON_FILE_LOCATION = os.path.join(
    JSON_DIRECTORY_NAME,
    JSON_FILE_NAME
)