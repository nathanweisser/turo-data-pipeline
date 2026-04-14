import requests
import json

# The specific ID from your uploaded layout file
DOC_ID = "0b523226-fef9-4dfa-b3c4-9f71d1ec1041"
SOURCE_URL = f"https://api.calculatorstudio.co/document/{DOC_ID}"

def translate_data():
    # Headers make the script look like a Chrome browser to avoid blocks
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }

    print("Fetching Turo data source...")
    response = requests.get(SOURCE_URL, headers=headers)
    
    if response.status_code != 200:
        print(f"Server Error: Received status code {response.status_code}")
        return

    try:
        raw_data = response.json()
    except Exception as e:
        print("Failed to parse initial JSON. The server might be blocking the request.")
        return

    # In v2.1, the 'cells' are stored as a string inside 'published_state'
    published_state = raw_data.get('published_state', {})
    cells_string = published_state.get('cells', '{}')
    
    # We must parse this string a second time to turn it into a dictionary
    try:
        cells = json.loads(cells_string)
    except Exception as e:
        print("Failed to parse the internal cells string.")
        cells = {}

    clean_data = {
        "hello_world": 99999,
        "debug_count": len(cells)
    }

    # Now we use the column-based logic to pair names and earnings
    for cell_id, cell_obj in cells.items():
        val = cell_obj.get('v')
        
        # Look for car names in Column C
        if isinstance(val, str) and cell_id.startswith('C'):
            row_num = ''.join(filter(str.isdigit, cell_id))
            
            # Look for annual earnings in Column J
            earnings_key = f"J{row_num}"
            if earnings_key in cells:
                e_val = cells[earnings_key].get('v')
                if isinstance(e_val, (int, float)):
                    car_key = val.strip().lower().replace(" ", "_")
                    clean_data[car_key] = int(e_val)

    with open('turo_data.json', 'w') as f:
        json.dump(clean_data, f, indent=2)
    
    print(f"Successfully translated {len(clean_data) - 2} vehicles.")

if __name__ == "__main__":
    translate_data()
