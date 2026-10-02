from alembic import op


revision = "f413304ea37e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
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
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS iss_enriched (
            id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            iss_data_id BIGINT NOT NULL,
            distance_km DECIMAL(12, 2) NOT NULL,
            country VARCHAR(128),
            city VARCHAR(128),
            body_of_water VARCHAR(128),
            FOREIGN KEY (iss_data_id) REFERENCES iss_data(id)
        );
    """)


def downgrade():
    op.execute("""
        DROP TABLE IF EXISTS iss_enriched;
    """)

    op.execute("""
        DROP TABLE IF EXISTS iss_data;
    """)