import pandas as pd
import requests
from urllib.parse import quote
import json

# Load the CSV file
df = pd.read_csv('lists/urls.csv')

# Ensure the tech directory exists
import os
if not os.path.exists('tech'):
    os.makedirs('tech')

# Loop through all URLs in the CSV
for url in df['url']:
    # Encode the URL
    encoded_url = quote(url, safe='')

    print(f"Processing URL: {url}")

    # Send the GET request
    response = requests.get(f'https://tech.gova11y.io/extract?url={encoded_url}')

    # Check the HTTP status code
    if response.status_code == 200:
        # If successful, append the data to the success.json file
        try:
            # Parse the JSON response
            data = response.json()

            # Check if the 'status' in 'urls' is 0, indicating a bad host
            url_data = list(data['urls'].values())[0]
            url_status = url_data.get('status')

            if url_status == 0:
                with open('tech/bad_host.json', 'a') as f:
                    json.dump(data, f)
                    f.write('\n')
                print(f"Bad Host: Data for URL {url} saved to bad_host.json.")
            else:
                # Open the JSON file in append mode
                with open('tech/success.json', 'a') as f:
                    # Write the JSON object to the file
                    json.dump(data, f)
                    # Write a newline character to separate JSON objects
                    f.write('\n')
                print(f"Success: Data for URL {url} saved to success.json.")

                # Save the cleaned URL (without http:// or https:// prefix) to complete.csv
                cleaned_url = url.replace('http://', '').replace('https://', '')
                with open('tech/complete.csv', 'a') as f:
                    f.write(f"{cleaned_url}\n")
                print(f"Success: Cleaned URL {cleaned_url} saved to complete.csv.")

        except json.JSONDecodeError:
            print(f"Failure: Could not decode JSON response for URL {url}")
    else:
        # If failed, append the URL to the failure.csv file
        with open('tech/failure.csv', 'a') as f:
            f.write(url + '\n')
        print(f"Failure: URL {url} saved to failure.csv. HTTP Status code: {response.status_code}")
