import requests
import json

SOURCE_URL = "https://api.calculatorstudio.co/document/turo-carculator-v2-0-C1IyJv75TfqzxJ9x0ewQQQ"

def translate_data():
    print("Fetching Turo data source...")
    response = requests.get(SOURCE_URL)
    raw_data = response.json()

    # The data is located inside a 'cells' dictionary
    cells = raw_data.get('cells', {})
    clean_data = {}

    # We need to find car names and their matched earnings.
    # In this structure, car names are often in column 'C' 
    # and estimated earnings are in column 'J'.
    
    # We iterate through all cells to find "Make Model" strings
    for cell_id, cell_data in cells.items():
        val = cell_data.get('v')
        
        # We are looking for strings that look like car names (e.g., "Cadillac Ats")
        if isinstance(val, str) and cell_id.startswith('C'):
            row_number = cell_id[1:] # Extract the row number (e.g., "2688")
            
            # Now look for the corresponding earnings in column 'J' of the same row
            earnings_cell = f"J{row_number}"
            if earnings_cell in cells:
                earnings_val = cells[earnings_cell].get('v')
                
                if isinstance(earnings_val, (int, float)):
                    # Create a clean key: "cadillac_ats"
                    car_key = val.replace(" ", "_").lower().strip()
                    clean_data[car_key] = int(earnings_val)

    # Save the file
    with open('turo_data.json', 'w') as f:
        json.dump(clean_data, f, indent=2)
    
    print(f"Successfully translated {len(clean_data)} vehicles.")

if __name__ == "__main__":
    translate_data()
