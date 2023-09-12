import pandas as pd

# Load the old and new CSV files
old_csv = pd.read_csv('raw/1_govt_urls_full.csv')
new_csv = pd.read_csv('raw/current-full.csv')

# Get unique domain types from both CSVs
old_domain_types = old_csv['Type of government'].dropna().unique()
new_domain_types = new_csv['Domain Type'].dropna().unique()

# Combine and deduplicate the lists of unique domain types
all_domain_types = set(old_domain_types.tolist() + new_domain_types.tolist())

# Save the unique domain types to a new CSV file
pd.DataFrame(all_domain_types, columns=['domain_type']).to_csv('lists/domain_types.csv', index=False)

print(f"Found {len(all_domain_types)} unique domain types.")
