import requests
import json

SOURCE_URL = "https://api.calculatorstudio.co/document/turo-carculator-v2-0-C1IyJv75TfqzxJ9x0ewQQQ"

def translate_data():
    print("Fetching Turo data source...")
    try:
        response = requests.get(SOURCE_URL, timeout=30)
        raw_data = response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    cells = raw_data.get('cells', {})
    clean_data = {
        "hello_world": 99999,  # TEST ENTRY: This proves the script ran and saved!
        "test_car": 12345
    }

    # Identify all rows that contain car names and numbers
    # We look for strings in column C (Make/Model) and numbers in column J (Earnings)
    # These coordinates are based on the Cadillac entry found in your HAR file.
    for cell_id, cell_obj in cells.items():
        val = cell_obj.get('v')
        
        # 1. Find a car name (usually in Column C)
        if isinstance(val, str) and cell_id.startswith('C'):
            row_num = cell_id[1:] # e.g., "2688" from "C2688"
            
            # 2. Look for the corresponding earning value in Column J of that same row
            earnings_key = f"J{row_num}"
            if earnings_key in cells:
                earnings_val = cells[earnings_key].get('v')
                
                # If we found a number, save it!
                if isinstance(earnings_val, (int, float)):
                    # Format name: "Cadillac Ats" -> "cadillac_ats"
                    clean_key = val.strip().lower().replace(" ", "_")
                    clean_data[clean_key] = int(earnings_val)

    # Save the output
    with open('turo_data.json', 'w') as f:
        json.dump(clean_data, f, indent=2)
    
    print(f"Successfully translated {len(clean_data)} vehicles (including hello_world).")

if __name__ == "__main__":
    translate_data()
