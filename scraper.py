import requests
import json

SOURCE_URL = "https://api.calculatorstudio.co/document/turo-carculator-v2-0-C1IyJv75TfqzxJ9x0ewQQQ"

def translate_data():
    print("Fetching Turo data source...")
    response = requests.get(SOURCE_URL)
    raw_data = response.json()
    cells = raw_data.get('cells', {})

    debug_dump = {
        "debug_status": "dumping_samples",
        "sample_cells": []
    }

    # Grab the first 100 cells that have text in them
    count = 0
    for cell_id, cell_obj in cells.items():
        val = cell_obj.get('v')
        if val and isinstance(val, str) and len(val) > 1:
            debug_dump["sample_cells"].append(f"{cell_id}: {val}")
            count += 1
        if count >= 100:
            break

    # Also grab any cell that looks like a high dollar amount (e.g., 5000+)
    debug_dump["potential_earnings"] = []
    e_count = 0
    for cell_id, cell_obj in cells.items():
        val = cell_obj.get('v')
        if isinstance(val, (int, float)) and 3000 < val < 50000:
            debug_dump["potential_earnings"].append(f"{cell_id}: {val}")
            e_count += 1
        if e_count >= 50:
            break

    with open('turo_data.json', 'w') as f:
        json.dump(debug_dump, f, indent=2)
    
    print("Sample data dumped. Check your URL.")

if __name__ == "__main__":
    translate_data()
