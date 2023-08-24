import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import os

URL = 'https://news.ycombinator.com/item?id=36956867'

print("Sending request to HackerNews...")

response = requests.get(URL)

if response.status_code == 200:
    print("Successfully fetched the webpage!")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    search_terms = [
        "data science", "machine learning engineer", "statistical modeler", "AI specialist",
        "data engineering", "big data engineer", "data infrastructure", "ETL developer",
        "data analysis", "data analytics", "business analyst", "BI analyst", 'data scientists'
    ]
    comments = soup.find_all('span', class_='commtext c00')
    matched_jobs = []

    print("Extracting job listings...")
    for comment in comments:
        for term in search_terms:
            if term in comment.text.lower():
                matched_jobs.append({"Job Title": term, "Description": comment.text})
                break

    print(f"Found {len(matched_jobs)} job listings!")
else:
    print(f"Failed to fetch the webpage. HTTP Status Code: {response.status_code}")

print("Waiting for 30 seconds to respect crawl delay...")
time.sleep(30)  # Respecting the robots.txt instructions
print("Done waiting!")

df = pd.DataFrame(matched_jobs)

csv_file = 'job_listings.csv'
if os.path.exists(csv_file):
    df.to_csv(csv_file, mode='a', header=False, index=False)
else:
    df.to_csv(csv_file, index=False)

print(f"Data saved to {csv_file}!")