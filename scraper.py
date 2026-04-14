import requests
import json

SOURCE_URL = "https://api.calculatorstudio.co/document/turo-carculator-v2-0-C1IyJv75TfqzxJ9x0ewQQQ"

def translate_data():
    print("Fetching Turo data source...")
    try:
        # Increased timeout for the large file
        response = requests.get(SOURCE_URL, timeout=60)
        raw_data = response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    cells = raw_data.get('cells', {})
    clean_data = {
        "last_updated": "2026-04-14",
        "debug_total_cells": len(cells)
    }

    # Identify all rows by scanning the cell keys (e.g., "C5230" -> row 5230)
    rows = {}
    for cell_id, cell_obj in cells.items():
        # Extract the letter (column) and number (row)
        col = "".join([c for c in cell_id if c.isalpha()])
        row = "".join([c for c in cell_id if c.isdigit()])
        
        if row not in rows:
            rows[row] = {}
        rows[row][col] = cell_obj.get('v')

    # Now we process each row to find car names and their earnings
    for row_id, columns in rows.items():
        # Standard car names in this data are in Column C
        car_name = columns.get('C')
        
        if isinstance(car_name, str) and len(car_name) > 3:
            # Look for earnings in Columns H, I, or J (common for this tool)
            for col_letter in ['H', 'I', 'J', 'K']:
                val = columns.get(col_letter)
                # If we find a number that looks like annual earnings
                if isinstance(val, (int, float)) and 3000 < val < 60000:
                    clean_key = car_name.strip().lower().replace(" ", "_")
                    clean_data[clean_key] = int(val)
                    break

    # Save the finalized JSON
    with open('turo_data.json', 'w') as f:
        json.dump(clean_data, f, indent=2)
    
    print(f"Successfully translated {len(clean_data) - 2} vehicles.")

if __name__ == "__main__":
    translate_data()
