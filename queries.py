from config import DB_NAME


CREATE_DATABASE = f"CREATE DATABASE {DB_NAME}"


CREATE_TABLE_ISS_DATA = """
    CREATE TABLE IF NOT EXISTS iss_data (
        id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        iss_id DECIMAL(10, 2) NOT NULL,
        latitude DECIMAL(10, 2) NOT NULL,
        longitude DECIMAL(10, 2) NOT NULL,
        altitude DECIMAL(10, 2) NOT NULL,
        velocity DECIMAL(10, 2) NOT NULL,
        visibility VARCHAR(32) NOT NULL,
        footprint DECIMAL(10, 2) NOT NULL,
        timestamp BIGINT NOT NULL,
        daynum DECIMAL(10, 2) NOT NULL,
        solar_lat DECIMAL(10, 2) NOT NULL,
        solar_lon DECIMAL(10, 2) NOT NULL,
        units VARCHAR(12) NOT NULL
    );
"""

CREATE_TABLE_ISS_ENRICHED = """
    CREATE TABLE IF NOT EXISTS iss_enriched (
        id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        iss_data_id BIGINT NOT NULL,
        distance_km DECIMAL(12, 2) NOT NULL,
        country VARCHAR(128),
        city VARCHAR(128),
        body_of_water VARCHAR(128),
        FOREIGN KEY (iss_data_id) REFERENCES iss_data(id)
    );
"""

INSERT_INTO_ISS_DATA = """
    INSERT INTO iss_data (
        iss_id, latitude, longitude, altitude, velocity, visibility, 
        footprint, timestamp, daynum, solar_lat, solar_lon, units
    ) VALUES (
        %(id)s, %(latitude)s, %(longitude)s, %(altitude)s, %(velocity)s, %(visibility)s, 
        %(footprint)s, %(timestamp)s, %(daynum)s, %(solar_lat)s, %(solar_lon)s, %(units)s
    ) RETURNING id;
"""

INSERT_ISS_ENRICHED = """
    INSERT INTO iss_enriched (
        iss_data_id, distance_km, country, city, body_of_water
    ) VALUES (
        %(iss_data_id)s, %(distance_km)s, %(country)s, %(city)s, %(body_of_water)s
    );
"""

SELECT_LAST_TIMESTAMP = "SELECT timestamp FROM iss_data ORDER BY timestamp DESC LIMIT 1;"
SELECT_HIGHEST_VELOCITY = "SELECT MAX(velocity) AS highest_velocity FROM iss_data;"
SELECT_VISIBILITY_COUNT = "SELECT visibility, COUNT(*) FROM iss_data GROUP BY visibility;"