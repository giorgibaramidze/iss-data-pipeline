from config import DB_NAME


CREATE_DATABASE = f"CREATE DATABASE {DB_NAME}"


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