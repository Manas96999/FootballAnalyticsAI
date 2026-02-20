import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

def fetch_and_save_matches():
    load_dotenv() # Load environment variables from .env file
    # Load API token from environment variable
    # It's recommended to set this in your .env file and load it using a library like python-dotenv
    # For now, we'll just use os.getenv directly.
    API_TOKEN = os.getenv('FOOTBALL_DATA_API_KEY')

    if not API_TOKEN:
        print("Error: FOOTBALL_DATA_API_KEY environment variable not set.")
        print("Please get a free API key from https://www.football-data.org/ and set it in your .env file.")
        return

    # Define the API endpoint for matches
    URI = 'https://api.football-data.org/v4/matches'
    HEADERS = {
        'X-Auth-Token': API_TOKEN
    }

    try:
        print(f"Fetching data from {URI}...")
        response = requests.get(URI, headers=HEADERS)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        data = response.json()

        # Define the path to save the raw JSON data
        output_dir = 'data/raw/'
        os.makedirs(output_dir, exist_ok=True) # Ensure the directory exists

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = os.path.join(output_dir, f'matches_raw_{timestamp}.json')

        with open(output_filename, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"Successfully fetched and saved raw match data to {output_filename}")
        print(f"Total matches found: {data.get('count', 'N/A')}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.text}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"Error decoding JSON response: {json_err}")
        print(f"Raw response: {response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    fetch_and_save_matches()
