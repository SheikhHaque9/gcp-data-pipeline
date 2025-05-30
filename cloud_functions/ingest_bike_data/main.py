import requests
import os

def main(event, context):
    api_key = os.environ.get("TFL_API_KEY")
    response = requests.get(f"https://api.tfl.gov.uk/BikePoint/?app_id={api_key}")
    print(response.json())  # Placeholder for storing in Cloud SQL





