import pandas as pd # type: ignore
import os
from plate_detecting import extract_plate_text

# Directory of the images
images_dir = os.path.join('..', 'data', 'images')

# Function to process the CSV files from the radars
def process_radar_data(input_csv, radar_number, images_dir):
    # Read the CSV file
    df = pd.read_csv(input_csv)

    # Add "Plate" and "Radar" columns
    df['Plate'] = df['image'].apply(lambda img: extract_plate_text(os.path.join(images_dir, img)))
    df['Radar'] = radar_number

    return df

# Project directories
base_dir = os.path.dirname(os.path.abspath(__file__))  # Base directory of the script
data_dir = os.path.join(base_dir, '..', 'data')  # Parent directory to 'data'
images_dir = os.path.join(data_dir, 'images')  # Images folder
raw_data_dir = os.path.join(data_dir, 'raw')  # Folder with the original CSV files
processed_data_dir = os.path.join(data_dir, 'processed')  # Folder for the processed CSV files

# Ensure that the output directory exists
os.makedirs(processed_data_dir, exist_ok=True)

# Process the data from both radars and combine them into a single DataFrame
df_radar_1 = process_radar_data(os.path.join(raw_data_dir, 'data_radar_1.csv'), 1, images_dir)
df_radar_2 = process_radar_data(os.path.join(raw_data_dir, 'data_radar_2.csv'), 2, images_dir)

# Combine the DataFrames from both radars
combined_df = pd.concat([df_radar_1, df_radar_2], ignore_index=True)

# Full path for the combined CSV file
combined_csv_path = os.path.join(processed_data_dir, 'combined_plate_data.csv')

# Save the combined DataFrame into a CSV file
combined_df.to_csv(combined_csv_path, index=False)