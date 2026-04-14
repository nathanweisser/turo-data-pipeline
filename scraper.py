import requests
import json

# The URL from your HAR file (Calculator Studio document)
SOURCE_URL = "https://api.calculatorstudio.co/document/turo-carculator-v2-0-C1IyJv75TfqzxJ9x0ewQQQ"

def translate_data():
    print("Fetching Turo data source...")
    response = requests.get(SOURCE_URL)
    raw_data = response.json()

    # This dictionary will hold our clean "Car: Price" pairs
    clean_data = {}

    # Calculator Studio stores data in a 'values' list. 
    # We iterate through to find car names and their corresponding earnings.
    # Note: We use lowercase and underscores to make matching in the extension easier.
    
    values = raw_data.get('values', [])
    
    # Based on the Cadillac CT6 example in your HAR:
    # We are looking for the 'Make/Model' string and the 'Earnings' number.
    for i in range(len(values)):
        item = values[i]
        # Logic to identify a car name row (Adjusting based on HAR structure)
        if isinstance(item, str) and len(item) > 2:
            # We look ahead for the next number which is usually the annual profit
            for j in range(i + 1, i + 5): # Look in the next few cells
                if j < len(values) and (isinstance(values[j], int) or isinstance(values[j], float)):
                    car_key = item.replace(" ", "_").lower()
                    clean_data[car_key] = int(values[j])
                    break

    # Save the tiny translated file
    with open('turo_data.json', 'w') as f:
        json.dump(clean_data, f)
    
    print(f"Successfully translated {len(clean_data)} vehicles.")

if __name__ == "__main__":
    translate_data()
