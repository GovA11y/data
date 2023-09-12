import pandas as pd
import requests
from urllib.parse import quote
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables
API_URL = os.environ.get('API_URL', 'http://localhost:3000')

# Load the CSV file starting from row 4500
df = pd.read_csv('lists/clean.csv', skiprows=range(1, 4500))

# Create the results directory if it doesn't exist
if not os.path.exists('local'):
    os.makedirs('local')

# Create a new column 'url' using the 'Domain Name' column
df['url'] = 'http://' + df['domain_name'].str.lower()

# Loop through all URLs in the dataframe
for _, row in df.iterrows():
    domain_name = row['domain_name']
    url = row['url']

    # Encode the URL
    encoded_url = quote(url, safe='')

    print(f"Processing URL: {url}")

    # Send the GET request
    response = requests.get(f'{API_URL}/extract?url={encoded_url}')

    # Check the HTTP status code
    if response.status_code == 200:
        try:
            data = response.json()
            url_data = list(data['urls'].values())[0]
            url_status = url_data.get('status')

            if url_status == 0:
                with open('local/bad_host.json', 'a') as f:
                    json.dump(data, f)
                    f.write('\n')
                print(f"Bad Host: Data for URL {url} saved to bad_host.json.")
            else:
                with open('local/success.json', 'a') as f:
                    json.dump(data, f)
                    f.write('\n')
                print(f"Success: Data for URL {url} saved to success.json.")

                with open('local/complete.csv', 'a') as f:
                    f.write(f"{domain_name},{url}\n")
                print(f"Success: Domain {domain_name} and URL {url} saved to complete.csv.")
        except json.JSONDecodeError:
            print(f"Failure: Could not decode JSON response for URL {url}")
    else:
        with open('local/failure.csv', 'a') as f:
            f.write(url + '\n')
        print(f"Failure: URL {url} saved to failure.csv. HTTP Status code: {response.status_code}")
