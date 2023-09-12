import pandas as pd

# Load the old and new CSV files
old_csv = pd.read_csv('raw/1_govt_urls_full.csv')
print(old_csv.columns)

new_csv = pd.read_csv('raw/current-full.csv')

# Create a dictionary to map 'Domain Type' and 'Type of Government' to 'agency_type'
domain_type_to_agency_type = {
    'City': 'city',
    'County': 'county',
    'Independent Intrastate': 'independent_intrastate',
    'State': 'state',
    'Federal - Legislative': 'federal',
    'Federal - Executive': 'federal',
    'Federal - Judicial': 'federal',
    'Native Sovereign Nation / Tribal': 'native_sovereign_nation_tribal',
    'Regional': 'regional',
    'Tribal': 'tribal',
    'Interstate': 'interstate',
    'Local': 'local',
    'Quasigovernmental': 'quasigovernmental',
    '"Level unclear, see note"': 'see_note',
    'Federal': 'federal'
}

domain_type_to_branch = {
    'Federal - Legislative': 'legislative',
    'Federal - Executive': 'executive',
    'Federal - Judicial': 'judicial',
    'Federal': 'unspecified'
}

# Apply 'agency_type' and 'branch' mappings to both old and new CSVs
old_csv['agency_type'] = old_csv['Type of government'].map(domain_type_to_agency_type)
old_csv['branch'] = old_csv['Type of government'].map(domain_type_to_branch)


new_csv['agency_type'] = new_csv['Domain Type'].map(domain_type_to_agency_type)
new_csv['branch'] = new_csv['Domain Type'].map(domain_type_to_branch)

# Define the new schema with snake_case column names
schema = [
    "domain_name", "agency_organization", "maintaining_office",
    "use_case", "city", "state", "security_contact_email",
    "comments", "link", "date_added", "agency_type", "branch"
]

# Create a new DataFrame with the new schema
merged_df = pd.DataFrame(columns=schema)

# Mapping the columns from the old and new dataframes to the new schema with snake_case names
old_mappings = {
    "Domain name": "domain_name",
    "Agency": "agency_organization",
    "Maintaining office": "maintaining_office",
    "Use case": "use_case",
    "State": "state",
    "Comments": "comments",
    "Link": "link",
    "Date Added": "date_added",
}

new_mappings = {
    "Domain Name": "domain_name",
    "Agency": "agency_organization",
    "Organization": "maintaining_office",
    "City": "city",
    "State": "state",
    "Security Contact Email": "security_contact_email",
}

# Transform the dataframes to have the new schema with snake_case names
old_csv_transformed = old_csv.rename(columns=old_mappings)
new_csv_transformed = new_csv.rename(columns=new_mappings)

# Use pd.concat to merge the dataframes
merged_df = pd.concat([old_csv_transformed, new_csv_transformed], ignore_index=True)

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('lists/all.csv', index=False)
