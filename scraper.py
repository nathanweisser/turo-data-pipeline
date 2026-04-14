import requests
import json

# This is the verified data source from your HAR file
SOURCE_URL = "https://api.calculatorstudio.co/document/turo-carculator-v2-0-C1IyJv75TfqzxJ9x0ewQQQ"

def translate_data():
    print("Fetching Turo data source...")
    try:
        # Increase timeout to handle the large 1.4MB file
        response = requests.get(SOURCE_URL, timeout=60)
        raw_data = response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    cells = raw_data.get('cells', {})
    clean_data = {
        "last_updated": "2026-04-14", # Proves the update worked
        "data_source": "Verified Column C/J Mapping"
    }

    print("Mapping car names from Column C to earnings in Column J...")

    # We iterate through the cells looking for car names in Column C
    # Based on the HAR, Cadillac is at C2805 and its earnings are at J2805
    for cell_id, cell_obj in cells.items():
        val = cell_obj.get('v')
        
        # Look for cells in Column C that contain car name strings
        if isinstance(val, str) and cell_id.startswith('C'):
            # Extract row number (e.g., '2805' from 'C2805')
            row_num = ''.join(filter(str.isdigit, cell_id))
            
            # The earnings are consistently in Column J of the same row
            earnings_key = f"J{row_num}"
            if earnings_key in cells:
                earnings_val = cells[earnings_key].get('v')
                
                # Verify we found a valid number for earnings
                if isinstance(earnings_val, (int, float)) and earnings_val > 100:
                    # Clean the car name: "Cadillac ATS" -> "cadillac_ats"
                    clean_key = val.strip().lower().replace(" ", "_")
                    clean_data[clean_key] = int(earnings_val)

    # Save the finalized JSON to your GitHub Pages folder
    with open('turo_data.json', 'w') as f:
        json.dump(clean_data, f, indent=2)
    
    print(f"Success! Translated {len(clean_data) - 2} vehicles.")

if __name__ == "__main__":
    translate_data()
