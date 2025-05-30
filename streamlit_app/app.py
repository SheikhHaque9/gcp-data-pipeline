# app.py
import streamlit as st
import requests
import pandas as pd

st.title("🚲 TfL BikePoint Live Dashboard")

# Get BikePoint data
url = "https://api.tfl.gov.uk/BikePoint"
response = requests.get(url)
data = response.json()

stations = []
for station in data:
    name = station["commonName"]
    bikes = next((p["value"] for p in station["additionalProperties"] if p["key"] == "NbBikes"), None)
    empty_docks = next((p["value"] for p in station["additionalProperties"] if p["key"] == "NbEmptyDocks"), None)
    stations.append({
        "Station": name,
        "Bikes": int(bikes),
        "Empty Docks": int(empty_docks)
    })

df = pd.DataFrame(stations)
st.dataframe(df)

# Optional: filter by station name
station_filter = st.text_input("Filter by station name")
if station_filter:
    st.dataframe(df[df["Station"].str.contains(station_filter, case=False)])

# Overview
st.header("Overview")
st.write(
    "This project builds a data pipeline on Google Cloud Platform (GCP) to collect, "
    "process, and store real-time bike availability data in London using the TfL BikePoint API. "
    "The architecture leverages key GCP services such as Cloud Scheduler, Pub/Sub, Cloud Functions, "
    "Cloud SQL, and Compute Engine to automate data ingestion, transformation, and visualization "
    "via this Streamlit web app."
)

# Architecture
st.header("Architecture")

st.subheader("1. Data Source")
st.write("Bike availability and station data is fetched from the Transport for London (TfL) BikePoint API.")

st.subheader("2. Data Ingestion")
st.write(
    "• A Cloud Scheduler job triggers every 30 minutes (CRON: */30 * * * *).\n"
    "• This scheduler publishes a message to a Pub/Sub topic (bike_ingestion).\n"
    "• A Cloud Function (ingest_bike_data) is triggered by this topic and fetches data from the API."
)

st.subheader("3. Data Processing")
st.write(
    "The Cloud Function processes the JSON data, extracts relevant fields, and prepares it for storage."
)

st.subheader("4. Data Storage")
st.write(
    "Processed data is inserted into a Cloud SQL (MySQL) database. "
    "Each record includes station-level info with a timestamp for tracking historical availability."
)

st.subheader("5. Data Visualization")
st.write(
    "This Streamlit web app queries the Cloud SQL database, loads the data into pandas DataFrames, "
    "and presents visual summaries such as:\n"
    "- Total available bikes and docks\n"
    "- Station-level details\n"
    "- Time-based trends"
)

# Tech Stack
st.header("Tech Stack")

st.subheader("Google Cloud Platform (GCP)")
st.write(
    "- Cloud Scheduler (for timed execution)\n"
    "- Pub/Sub (for messaging)\n"
    "- Cloud Functions (to fetch and process data)\n"
    "- Cloud SQL (MySQL database for storage)\n"
    "- Compute Engine (hosts the Streamlit app)"
)

st.subheader("External Services & Tools")
st.write(
    "- TfL BikePoint API (real-time data source)\n"
    "- Streamlit (Python-based visualization and deployment framework)\n"
    "- Terraform (Infrastructure-as-Code)"
)
