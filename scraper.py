import requests
import json

# These IDs were discovered in your HAR file
DOC_ID = "0b523226-fef9-4dfa-b3c4-9f71d1ec1041"
WORKBOOK_ID = "067650e1-79f4-465f-a79e-230edadffe45"
SOURCE_URL = f"https://api.calculatorstudio.co/document/{DOC_ID}/workbook/{WORKBOOK_ID}/body?is_embedded=true"

def translate_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    print("Fetching deep Turo workbook data...")
    response = requests.get(SOURCE_URL, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Could not reach data source (Status {response.status_code})")
        return

    data = response.json()
    
    # Locate the "Data" sheet which contains the car-to-dollar mappings
    sheets = data.get('sheets', [])
    data_sheet = next((s for s in sheets if s['name'] == 'Data'), None)
    
    if not data_sheet:
        print("Error: Could not find the 'Data' sheet in the workbook.")
        return

    cells = data_sheet.get('cells', {})
    clean_data = {
        "status": "online",
        "last_updated": "2026-04-14"
    }

    # We group cells by row to make matching easier
    rows = {}
    for cell_id, cell_obj in cells.items():
        col = "".join([c for c in cell_id if c.isalpha()])
        row = "".join([c for c in cell_id if c.isdigit()])
        if row not in rows:
            rows[row] = {}
        rows[row][col] = cell_obj.get('v')

    print(f"Processing {len(rows)} rows of data...")

    for row_id, cols in rows.items():
        # We only want 'National Average' data to avoid duplicates for every city
        if cols.get('A') == 'National Average':
            car_name = cols.get('C') # Car Name is in Column C
            earnings = cols.get('J') # Annual Earnings is in Column J
            
            if isinstance(car_name, str) and isinstance(earnings, (int, float)):
                # Key format: "toyota_4runner"
                clean_key = car_name.strip().lower().replace(" ", "_")
                clean_data[clean_key] = int(earnings)

    # Save the file for your GitHub Pages
    with open('turo_data.json', 'w') as f:
        json.dump(clean_data, f, indent=2)
    
    print(f"Successfully mapped {len(clean_data) - 2} vehicles from the national average list.")

if __name__ == "__main__":
    translate_data()
