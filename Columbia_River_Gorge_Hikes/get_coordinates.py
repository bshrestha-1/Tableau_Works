import pandas as pd
import requests
import time

# Google Maps Geocoding API endpoint
api_endpoint = "https://maps.googleapis.com/maps/api/geocode/json"

# API key
api_key = "Your key"

# Input CSV file
input_file = "hiking_trails.csv"

# Output CSV file
output_file = "hiking_trails_geocoded.csv"

# Define a function to geocode a trail
def geocode_trail(trail_name):
    # Construct the API request
    params = {
        "address": trail_name,
        "key": api_key
    }

    try:
        # Send the request and get the response
        response = requests.get(api_endpoint, params=params)

        # Check if the response was successful
        if response.status_code == 200:
            # Parse the response
            data = response.json()

            # Extract the latitude and longitude coordinates
            if data["status"] == "OK":
                latitude = data["results"][0]["geometry"]["location"]["lat"]
                longitude = data["results"][0]["geometry"]["location"]["lng"]
                return latitude, longitude
            elif data["status"] == "ZERO_RESULTS":
                print(f"Failed to geocode trail: {trail_name} (API status: ZERO_RESULTS)")
                return None, None
            else:
                print(f"Failed to geocode trail: {trail_name} (API status: {data['status']})")
                return None, None
        else:
            print(f"Failed to geocode trail: {trail_name} (HTTP status: {response.status_code})")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Failed to geocode trail: {trail_name} (Request error: {e})")
        return None, None

# Read the input CSV file
df = pd.read_csv(input_file)

# Geocode each trail and add the coordinates to the dataframe
df["Latitude"] = None
df["Longitude"] = None

for index, row in df.iterrows():
    trail_name = row[0]  # Use the first column as the trail name
    latitude, longitude = geocode_trail(trail_name)

    if latitude and longitude:
        df.loc[index, "Latitude"] = latitude
        df.loc[index, "Longitude"] = longitude

    # Add a delay between requests
    time.sleep(1)

# Write the geocoded dataframe to the output CSV file
df.to_csv(output_file, index=False)
