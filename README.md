# gcp-tfl-pipeline

Overview

This project builds a data pipeline on Google Cloud Platform (GCP) to collect, process, and store real-time bike availability data in London using the TfL BikePoint API. The architecture leverages key GCP services such as Cloud Scheduler, Pub/Sub, Cloud Functions, Cloud SQL, and Compute Engine to automate data ingestion, transformation, and visualization via this Streamlit web app.
Architecture
1. Data Source

Bike availability and station data is fetched from the Transport for London (TfL) BikePoint API.
2. Data Ingestion

• A Cloud Scheduler job triggers every hour (CRON: 0 * * * *). • This scheduler publishes a message to a Pub/Sub topic (bike_ingestion). • A Cloud Function (ingest_bike_data) is triggered by this topic and fetches data from the API.
3. Data Processing

The Cloud Function processes the JSON data, extracts relevant fields, and prepares it for storage.
4. Data Storage

Processed data is inserted into a Cloud SQL (MySQL) database. Each record includes station-level info with a timestamp for tracking historical availability.
5. Data Visualization

This Streamlit web app queries the Cloud SQL database, loads the data into pandas DataFrames, and presents visual summaries such as:

    Total available bikes and docks
    Station-level details
    Time-based trends

Tech Stack
Google Cloud Platform (GCP)

    Cloud Scheduler (for timed execution)
    Pub/Sub (for messaging)
    Cloud Functions (to fetch and process data)
    Cloud SQL (MySQL database for storage)
    Compute Engine (hosts the Streamlit app)

External Services & Tools

    TfL BikePoint API (real-time data source)
    Streamlit (Python-based visualization and deployment framework)
    Terraform (Infrastructure-as-Code)

