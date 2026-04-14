import requests
import json

# The URL from your HAR file's successful data load
SOURCE_URL = "https://api.calculatorstudio.co/document/0b523226-fef9-4dfa-b3c4-9f71d1ec1041"

def translate_data():
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(SOURCE_URL, headers=headers)
    raw_json = response.json()
    
    # Extract the nested cells from the 'published_state'
    cells_str = raw_json.get('published_state', {}).get('cells', '{}')
    cells = json.loads(cells_str)
    
    clean_data = {}

    for cell_id, cell_obj in cells.items():
        val = cell_obj.get('v')
        
        # We target Column C for the primary car name
        if isinstance(val, str) and cell_id.startswith('C'):
            row_num = ''.join(filter(str.isdigit, cell_id))
            
            # The earnings are consistently in Column J (calculated profit) 
            # or Column H (base revenue)
            earnings_cell = f"J{row_num}"
            if earnings_cell in cells:
                earnings = cells[earnings_cell].get('v')
                if isinstance(earnings, (int, float)):
                    # Store with a normalized key for your extension
                    name_key = val.strip().lower().replace(" ", "_")
                    clean_data[name_key] = int(earnings)

    # Manual check for the 4Runner in the output
    if "toyota_4runner" in clean_data:
        print(f"Verified: Toyota 4Runner earnings are ${clean_data['toyota_4runner']}")

    with open('turo_data.json', 'w') as f:
        json.dump(clean_data, f, indent=2)

if __name__ == "__main__":
    translate_data()
