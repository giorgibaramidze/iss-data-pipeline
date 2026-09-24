# 🚀 ISS & Geocoding Pipeline: Real-Time Satellite Tracking & Spatial Analytics

An automated ETL pipeline that tracks the International Space Station in real time, converting raw orbital telemetry into human-readable geographical location data and distance metrics. Built using pure Object-Oriented Python and PostgreSQL without an ORM, it is designed for data engineers and developers practicing clean software architecture, API integration, and relational database persistence.

## ✨ Features

- Decoupled Data Lake Storage:** Ingests untouched API JSON responses directly into a local data lake file to preserve raw telemetry history.
- Geographical & Orbital Analytics:** Translates spatial coordinates into countries, cities, or bodies of water using reverse geocoding while computing linear distance traveled based on orbital velocity.
- Relational Persistence & SQL Analytics:** Stores telemetry in PostgreSQL (`iss_data`) and transformed spatial metrics in a child table (`iss_enriched`) with handcrafted, ORM-free SQL queries.
- Structured File & Console Logging:** Replaces standard print statements with structured, timestamped logs saved automatically to file and console.

## 🛠️ Prerequisites

Before running this application, make sure you have the following installed:
- Python 3.9+
- PostgreSQL

## 📦 Installation

Follow these steps to set up the development environment:

 **Clone the repository and run following commands:**
   - git clone https://github.com/giorgibaramidze/iss-data-pipeline.git
   - cd iss-tracker
   - python3 -m venv .venv // create virtual envoirment
   - source .venv/bin/activate
   - pip install -r requirements.txt //install dependencies also
   - python main.py

   - Do not forget fill .env according to .env-example
