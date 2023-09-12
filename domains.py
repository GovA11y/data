import pandas as pd
from urllib.parse import urlparse

# Load the CSV file
df = pd.read_csv('lists/all.csv')

# Define a function to extract domain name from a URL
def extract_domain(url):
    if pd.notna(url):
        domain = urlparse(url).netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    return ""

# Create a new column with domain names extracted from the 'link' column
df['domain_name'] = df.apply(lambda row: extract_domain(row['link']) if pd.notna(row['link']) else row['domain_name'].lower(), axis=1)

# Drop duplicate rows based on the 'domain_name' column
df.drop_duplicates(subset='domain_name', keep='first', inplace=True)

# Save the modified DataFrame to a new CSV file
df.to_csv('lists/clean.csv', index=False, columns=[
    'domain_name', 'agency_organization', 'maintaining_office',
    'use_case', 'agency_type', 'branch', 'state',
    'comments', 'link', 'date_added',
    'city', 'security_contact_email'
])
