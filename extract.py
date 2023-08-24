import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import os

URL = 'https://news.ycombinator.com/item?id=36956867'

def extract_job_postings():
    response = requests.get(URL)
    
    # If the request is unsuccessful, return an empty list
    if response.status_code != 200:
        print(f"Failed to fetch the webpage. HTTP Status Code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    
    search_terms = [
        "data science", "machine learning engineer", "statistical modeler", "AI specialist",
        "data engineering", "big data engineer", "data infrastructure", "ETL developer",
        "data analysis", "data analytics", "business analyst", "BI analyst", 'data scientists'
    ]
    
    comments = soup.find_all('span', class_='commtext c00')
    matched_jobs = []

    for comment in comments:
        user_posted_element = comment.find_previous('span', class_='age')
        posted_date = None
        
        if user_posted_element and 'title' in user_posted_element.attrs:
            posted_date = user_posted_element['title'].split('T')[0]  # Extracting just the date part
        
        for term in search_terms:
            if term in comment.text.lower():
                matched_jobs.append({
                    "Job Title": term,
                    "Posted Date": posted_date, 
                    "Description": comment.text
                })
                break

    return matched_jobs

print("Sending request to HackerNews...")
matched_jobs = extract_job_postings()
print(f"Found {len(matched_jobs)} job listings!")

df = pd.DataFrame(matched_jobs)

csv_file = 'job_listings.csv'
if os.path.exists(csv_file):
    df.to_csv(csv_file, mode='a', header=False, index=False)
else:
    df.to_csv(csv_file, index=False)

print(f"Data saved to {csv_file}!")

# Respecting the robots.txt instructions
print("Waiting for 30 seconds to respect crawl delay...")
time.sleep(30)
print("Done waiting!")
