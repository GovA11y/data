import pandas as pd

# Load the clean CSV file
df = pd.read_csv('lists/clean.csv')

# Select only the 'domain_name' column
domain_name_df = df[['domain_name']]

# Add "http://" before each domain name
domain_name_df['domain_name'] = 'http://' + domain_name_df['domain_name']

# Save the 'domain_name' column to a new CSV file
domain_name_df.to_csv('lists/urls.csv', index=False)

