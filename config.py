from dotenv import dotenv_values
import os

config = dotenv_values()
OPENCAGE_API_KEY=config["OPENCAGE_API_KEY"]

DB_HOST=config["DB_HOST"]
DB_NAME=config["DB_NAME"]
DB_USER=config["DB_USER"]
DB_PASSWORD=config["DB_PASSWORD"]
DB_PORT=config["DB_PORT"]
JSON_FILE_NAME=config.get("JSON_FILE_NAME", "JSONData.json")
JSON_DIRECTORY_NAME=config.get("JSON_DIRECTORY_NAME", "storage/")
