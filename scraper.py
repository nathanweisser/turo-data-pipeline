import requests
import json

# The specific Document ID for the Turo Carculator v2.1
DOC_ID = "0b523226-fef9-4dfa-b3c4-9f71d1ec1041"
SOURCE_URL = f"https://api.calculatorstudio.co/document/{DOC_ID}"

def translate_data():
    # Headers to mimic a standard browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }

    print("Fetching Turo data source...")
    response = requests.get(SOURCE_URL, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Server returned status {response.status_code}")
        return

    try:
        raw_json = response.json()
    except Exception as e:
        print(f"Failed to parse initial JSON: {e}")
        return

    # In v2.1, the car data is a string inside the 'published_state' key
    ps = raw_json.get('published_state', {})
    cells_str = ps.get('cells', '{}')
    
    # We must parse the internal string to turn it into a searchable dictionary
    try:
        cells = json.loads(cells_str)
    except Exception as e:
        print(f"Failed to parse internal cells string: {e}")
        cells = {}

    clean_data = {
        "status": "success",
        "cell_count": len(cells)
    }

    print(f"Searching {len(cells)} cells for vehicle data...")

    # Iterate through the grid to find car names and earnings
    for cell_id, cell_obj in cells.items():
        val = cell_obj.get('v')
        
        # Column C contains the clean car names (e.g., "Toyota 4Runner")
        if isinstance(val, str) and cell_id.startswith('C'):
            row_num = ''.join(filter(str.isdigit, cell_id))
            
            # Column J contains the calculated annual earnings
            earnings_cell = f"J{row_num}"
            if earnings_cell in cells:
                earnings = cells[earnings_cell].get('v')
                
                # Verify we have a valid number for profit
                if isinstance(earnings, (int, float)):
                    # Format: "Toyota 4Runner" -> "toyota_4runner"
                    name_key = val.strip().lower().replace(" ", "_")
                    clean_data[name_key] = int(earnings)

    # Save the output to the file GitHub Pages will host
    with open('turo_data.json', 'w') as f:
        json.dump(clean_data, f, indent=2)
    
    print(f"Successfully mapped {len(clean_data) - 2} vehicles.")

if __name__ == "__main__":
    translate_data()
