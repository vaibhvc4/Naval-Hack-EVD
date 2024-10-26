import pandas as pd
import json

# Load JSON data
with open('test.json', 'r') as file:
    data = json.load(file)

processed_data = []
for entry in data:
    processed_data.append({
        "datetime": f"{entry["datetime"]}",
        "coords": entry["coords"],  
        "description": f"{entry["description"]}",
        "speed": f"{entry["speed"]}",
        "directions": f"{entry["directions"]}",
        "depth": f"{entry["depth"]}"
    })

df = pd.DataFrame(processed_data)

# Store list data as JSON strings in the CSV
df['coords'] = df['coords'].apply(json.dumps)
df.to_csv('report.csv', index=False)
