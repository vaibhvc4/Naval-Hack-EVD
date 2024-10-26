import json
import os
import csv

def parse_json_files(folder_path):
    data = []

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r') as file:
                content = file.read()
                # Split content by 'json' keyword and remove empty strings
                json_strings = [f.strip() for f in content.split('json') if f.strip()]
                
                for json_str in json_strings:
                    # Fix formatting issues and ensure proper JSON structure
                    json_str = json_str.strip().replace("\n", "").replace("   ", "")
                    try:
                        json_obj = json.loads(json_str)
                        data.append(json_obj)
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON: {e}")
                        print(f"Skipping JSON: {json_str}")

    return data

def write_to_csv(data, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        # Define the fieldnames for CSV
        fieldnames = ['name', 'type', 'significance', 'Coord A', 'Coord B', 'Coord C', 'Coord D']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for entry in data:
            row = {
                'name': entry.get('name', ''),
                'type': entry.get('type', ''),
                'significance': entry.get('significance', '')
            }
            coordinates = entry.get('coordinates', [])
            print(coordinates)
            
            # Ensure there are exactly 4 coordinates (8 lat/lon values)
            if len(coordinates) >= 4:
                row['Coord A'] = [coordinates[0]['lat'], coordinates[0]['lon']]
                row['Coord B'] = [coordinates[1]['lat'], coordinates[1]['lon']]
                row['Coord C'] = [coordinates[2]['lat'], coordinates[2]['lon']]
                row['Coord D'] = [coordinates[3]['lat'], coordinates[3]['lon']]
            else:
                row['Coord A'] = row['Coord B'] = row['Coord C'] = row['Coord D'] = ''
            
            writer.writerow(row)

if __name__ == "__main__":
    folder_path = 'Information-database'
    output_csv = 'output.csv'
    
    data = parse_json_files(folder_path)
    write_to_csv(data, output_csv)
