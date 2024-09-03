import pandas as pd # type: ignore
import numpy as np # type: ignore
import os

# Configuration
road_speed_limit = 60  # Speed limit in km/h
radar_distance_km = 1  # Distance between radars in km

# Project directories
base_dir = os.path.dirname(os.path.abspath(__file__))  # Base directory of the project
processed_data_dir = os.path.join(base_dir, '..', 'data', 'processed')  # Folder with the combined CSV
analysis_dir = os.path.join(base_dir, '..', 'analysis')  # Folder for the violations CSV

# Ensure that the analysis directory exists
os.makedirs(analysis_dir, exist_ok=True)

# Full path to the combined CSV file
combined_csv_path = os.path.join(processed_data_dir, 'combined_plate_data.csv')

# Read the combined CSV file
df = pd.read_csv(combined_csv_path)

# Convert the "Time" column to datetime type
df['Time'] = pd.to_datetime(df['Time'])

# Create the DataFrame for the violations CSV file
violation_df = pd.DataFrame(columns=[
    "Plate", "Time1", "Time2", "Time_difference", "Radar_distance(km)",
    "Speed(km/h)", "Road_Speed_Limit(km/h)", "Speeding"
])

# Find matching license plates between the two radars
plates = df['Plate'].unique()

for plate in plates:
    # Filter rows corresponding to the current license plate
    plate_df = df[df['Plate'] == plate]
    
    # If there are not exactly two entries for the license plate, continue to the next one
    if len(plate_df) != 2:
        continue

    # Separate rows by radar
    radar_1_row = plate_df[plate_df['Radar'] == 1]
    radar_2_row = plate_df[plate_df['Radar'] == 2]

    # Check that both radars have data for the license plate
    if radar_1_row.empty or radar_2_row.empty:
        continue

    # Extract data
    time1 = radar_1_row['Time'].values[0]
    time2 = radar_2_row['Time'].values[0]
    time_diff = time2 - time1  # Time difference in timedelta format
    time_diff_str = str(time_diff)  # Convert timedelta to string format HH:mm:ss

    # Calculate speed and determine if the speed limit is exceeded
    time_diff_hours = time_diff / np.timedelta64(1, 'h')  # Time difference in hours
    speed = radar_distance_km / time_diff_hours
    speed_rounded = round(speed, 2)  # Round speed to two decimals
    speeding = speed_rounded > road_speed_limit

    # Create a new DataFrame with the violation data
    new_row = pd.DataFrame([{
        "Plate": plate,
        "Time1": time1,
        "Time2": time2,
        "Time_difference": time_diff_str,  # Time in HH:mm:ss format
        "Radar_distance(km)": radar_distance_km,
        "Speed(km/h)": speed_rounded,  # Speed rounded to two decimals
        "Road_Speed_Limit(km/h)": road_speed_limit,
        "Speeding": speeding
    }])

    # Add the data to the violation DataFrame using pd.concat
    violation_df = pd.concat([violation_df, new_row], ignore_index=True)

# Full path for the violations CSV file
violation_csv_path = os.path.join(analysis_dir, 'traffic_violation.csv')

# Save the violation DataFrame to a CSV file
violation_df.to_csv(violation_csv_path, index=False)

# Report license plates that have exceeded the speed limit
speeding_plates = violation_df[violation_df['Speeding'] == True]
print("'traffic_violation' CSV has been created.")
print("Vehicles thas has exceedes the speed limit:")
for index, row in speeding_plates.iterrows():
    print(f"Plate: {row['Plate']}, Speed: {row['Speed(km/h)']:.2f} km/h")
