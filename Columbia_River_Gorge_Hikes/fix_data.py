import pandas as pd
import re

# Read the CSV file
df = pd.read_csv('HikingTrails_TheGorge.csv')

# Rename the columns
df = df.rename(columns={
    'Distance': 'Distance_miles',
    'High Point': 'High_Point_feet',
    'Elevation Gain': 'Elevation_feet'
})

# Function to extract the first number from a string
def extract_number(value):
    if pd.isna(value):
        return value
    match = re.search(r'\d+(\.\d+)?', str(value))
    return float(match.group()) if match else value

# Clean and convert the data
df['Distance_miles'] = df['Distance_miles'].apply(extract_number)
df['High_Point_feet'] = df['High_Point_feet'].apply(extract_number)
df['Elevation_feet'] = df['Elevation_feet'].apply(extract_number)

# Update Trail Type based on Distance
def update_trail_type(row):
    if pd.isna(row['Trail Type']):
        distance = str(row['Distance_miles'])
        if 'round trip' in distance:
            return 'Out and Back'
        elif 'loop' in distance:
            return 'Loop'
    return row['Trail Type']

df['Trail Type'] = df.apply(update_trail_type, axis=1)

# Save the modified DataFrame
df.to_csv('HikingTrails_TheGorge_modified.csv', index=False)

print(df.head())

