import json
import csv
import sys

# Check for correct usage
if len(sys.argv) != 3:
    print("Usage: python script.py input.json output.csv")
    sys.exit(1)

# Command line arguments
input_filename = sys.argv[1]
output_filename = sys.argv[2]

# Specify the keys you want to strip out
keys_to_strip = ["changed", "failed", "mtu", "shutdown", "state"]

# Process the data
def process_json(data, keys_to_strip):
    # Only retain the "gathered" key data
    gathered_data = data.get("gathered", [])
    
    # Filter out the unwanted keys from the gathered data
    for item in gathered_data:
        for key in keys_to_strip:
            item.pop(key, None)  # Remove the key if it exists

    return gathered_data

# Convert the filtered data to CSV
def write_to_csv(data, filename):
    if not data:
        print("No data to write to CSV.")
        return

    # Use the first dictionary to get CSV fieldnames
    fieldnames = data[0].keys()

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(data)

    print(f"Data written to {filename}")

# Read the JSON data from the input file
try:
    with open(input_filename, 'r') as json_file:
        data = json.load(json_file)
except FileNotFoundError:
    print(f"Error: File '{input_filename}' not found.")
    sys.exit(1)

# Process the JSON data
filtered_data = process_json(data, keys_to_strip)

# Write the filtered data to CSV using the output filename
write_to_csv(filtered_data, output_filename)
