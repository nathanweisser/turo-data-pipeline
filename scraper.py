import requests
import json

# The specific ID found in your uploaded JSON file
DOC_ID = "0b523226-fef9-4dfa-b3c4-9f71d1ec1041"
SOURCE_URL = f"https://api.calculatorstudio.co/document/{DOC_ID}/data"

def translate_data():
    print("Fetching Turo data source...")
    response = requests.get(SOURCE_URL)
    
    # If this fails, the data is likely in raw 'cells' format
    raw_data = response.json()
    clean_data = {"hello_world": 1}

    # This version of the API returns data in a 'data' array
    # or a 'cells' object depending on the session state.
    cells = raw_data.get('cells', {})
    
    for cell_id, cell_obj in cells.items():
        val = cell_obj.get('v')
        # Row-based matching for Car Names (Column C) and Earnings (Column J)
        if isinstance(val, str) and cell_id.startswith('C'):
            row_num = ''.join(filter(str.isdigit, cell_id))
            earnings_cell = f"J{row_num}"
            if earnings_cell in cells:
                e_val = cells[earnings_cell].get('v')
                if isinstance(e_val, (int, float)):
                    car_key = val.strip().lower().replace(" ", "_")
                    clean_data[car_key] = int(e_val)

    with open('turo_data.json', 'w') as f:
        json.dump(clean_data, f, indent=2)
    
    print(f"Success! Translated {len(clean_data)} vehicles.")

if __name__ == "__main__":
    translate_data()
