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
    total_docks = int(bikes) + int(empty_docks)
    occupancy_rate = round((int(bikes) / total_docks * 100) if total_docks > 0 else 0, 1)
    
    stations.append({
        "Station": name,
        "Bikes": int(bikes),
        "Empty Docks": int(empty_docks),
        "Total Docks": total_docks,
        "Occupancy Rate": occupancy_rate
    })

df = pd.DataFrame(stations)

# Quick stats
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Stations", len(df))
with col2:
    st.metric("Total Bikes Available", df["Bikes"].sum())
with col3:
    st.metric("Average Occupancy", f"{df['Occupancy Rate'].mean():.1f}%")

# Simple bar chart showing top 15 stations by bikes available
st.subheader("Top 15 Stations by Available Bikes")
top_stations = df.nlargest(15, 'Bikes')[['Station', 'Bikes']].set_index('Station')
st.bar_chart(top_stations)

# Data table
st.subheader("All Stations")
st.dataframe(df)

# Optional: filter by station name
station_filter = st.text_input("Filter by station name")
if station_filter:
    filtered_df = df[df["Station"].str.contains(station_filter, case=False)]
    st.subheader("Filtered Results")
    st.dataframe(filtered_df)

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

st.image("/streamlit_app/Diagram.png", caption="Architecture Diagram")

st.subheader("1. Data Source")
st.write("Bike availability and station data is fetched from the Transport for London (TfL) BikePoint API.")

st.subheader("2. Data Ingestion")
st.write(
    "• A Cloud Scheduler job triggers every hour (CRON: */60 * * * *).\n"
    "• This scheduler publishes a message to a Pub/Sub topic (bike_ingestion).\n"
    "• A Cloud Function (ingest_bike_data) is triggered by this topic and fetches data from the API."
)

st.subheader("3. Data Processing")
st.write(
    "• A Pub/Sub message is called by another Cloud Function to retrieve the fetched data.\n"
    "• The Cloud Function processes the data, extracts relevant fields, and prepares it for storage."
)

st.subheader("4. Data Storage")
st.write(
    "• Processed data is inserted into a Cloud SQL (PostgreSQL) database.\n"
    "• Each record includes station-level info with a timestamp for tracking historical availability."
)

st.subheader("5. Data Visualization")
st.write(
    "• This Streamlit web app queries the Cloud SQL database, loads the data into pandas DataFrames, and presents visual summaries such as:\n"
    "  - Total available bikes and docks\n"
    "  - Station-level details\n"
    "  - Time-based trends"
)

# Tech Stack
st.header("Tech Stack")

st.subheader("Google Cloud Platform (GCP)")
st.write(
    "- Cloud Scheduler (for timed execution)\n"
    "- Pub/Sub (for messaging)\n"
    "- Cloud Functions (to fetch and process data)\n"
    "- Cloud SQL (PostgreSQL database for storage)\n"
    "- Compute Engine (hosts the Streamlit app)"
)

st.subheader("External Services & Tools")
st.write(
    "- TfL BikePoint API (real-time data source)\n"
    "- Streamlit (Python-based visualization and deployment framework)\n"
    "- Terraform (Infrastructure-as-Code)"
)
