import requests
import json

# The URL from your HAR file
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
    
    # We initialize the JSON with some baseline info
    debug_results = {
        "debug_status": "searching",
        "hello_world": "I am alive",
        "found_cadillac_at": None,
        "nearby_values": []
    }

    print("Searching for Cadillac CT6 to identify coordinates...")
    
    # Iterate through every cell in the spreadsheet
    for cell_id, cell_obj in cells.items():
        val = str(cell_obj.get('v', ''))
        
        # Look for the Cadillac CT6 specifically
        if "Cadillac" in val and "CT6" in val:
            print(f"FOUND IT! Cadillac CT6 is in cell: {cell_id}")
            debug_results["found_cadillac_at"] = cell_id
            
            # Extract the row number (e.g., '2688' from 'C2688')
            row_num = ''.join(filter(str.isdigit, cell_id))
            
            # Scan columns A through M for this row to see where the money is
            columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
            for col in columns:
                target_cell = f"{col}{row_num}"
                if target_cell in cells:
                    cell_val = cells[target_cell].get('v')
                    debug_results["nearby_values"].append(f"{target_cell}: {cell_val}")

    # Save to your GitHub Pages JSON file
    with open('turo_data.json', 'w') as f:
        json.dump(debug_results, f, indent=2)
    
    print("Debug data saved. Check your GitHub Pages URL.")

if __name__ == "__main__":
    translate_data()
