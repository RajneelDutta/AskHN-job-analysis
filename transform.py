import pandas as pd
import os
import re

def extract_data(description):
    extracted = {
        "Company Name": None,
        "Location": None,
        "Type": None,
        "URL": None,
        "Salary Range": None,
        "Additional": None
    }
    split_description = description.split('|')
    if split_description:
        extracted["Company Name"] = split_description[0].strip()
        description = description.replace(extracted["Company Name"], "", 1)
    
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_pattern, description)
    if urls:
        extracted["URL"] = urls[0]
        description = description.replace(extracted["URL"], "") 

    location_pattern = r'\b(Remote|Onsite)\b.*?\|'
    location = re.search(location_pattern, description, re.IGNORECASE)
    if location:
        extracted["Location"] = location.group(0).strip('|')
        description = description.replace(extracted["Location"], "")

    type_pattern = r'\bFull[-\s]?Time\b|\bPart[-\s]?Time\b|FullTime|PartTime|FULL-TIME|PART-TIME'
    job_type = re.search(type_pattern, description, re.IGNORECASE)
    if job_type:
        extracted["Type"] = job_type.group(0)
        description = description.replace(extracted["Type"], "", 1)

    salary_pattern = r'(\$?\d+([,\d]+)?(\s?-?\s?\$?\d+([,\d]+)?K?\+?)?)'
    salary = re.search(salary_pattern, description, re.IGNORECASE)
    if salary and ('$' in salary.group(0) or 'K' in salary.group(0)):
        extracted["Salary Range"] = salary.group(0)
        description = description.replace(extracted["Salary Range"], "", 1)
    else:
        extracted["Salary Range"] = None

    extracted["Additional"] = description.strip()

    return extracted

df = pd.read_csv('data/job_listings.csv')

extracted_details = df['Description'].apply(extract_data).apply(pd.Series)

df_transformed = pd.concat([df.drop(columns=['Description']), extracted_details], axis=1)
#print(df_transformed.columns[1])

csv_file_transformed = 'data/job_listings_transformed.csv'
if os.path.exists(csv_file_transformed):
    df_transformed.to_csv(csv_file_transformed, mode='a', header=False, index=False)
else:
    df_transformed.to_csv(csv_file_transformed, index=False)

print(f"Data saved to {csv_file_transformed}!")
