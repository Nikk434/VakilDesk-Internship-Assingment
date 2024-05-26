from bs4 import BeautifulSoup
import os
import pymongo
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv("D:\VakilDesk\cred\.env")

# Read the HTML file
file_path = "D:\VakilDesk\output_2\page_1.html"
with open(file_path, "r", encoding="utf-8") as f:
    html_doc = f.read()

# Parse the HTML document with BeautifulSoup
soup = BeautifulSoup(html_doc, 'html.parser')

# Extract title
title = soup.title.string
print(title)

# Extract nav elements
nav = soup.find_all(class_="nav-link")
nav_links = [link.get_text() for link in nav]
for link in nav_links:
    print(link)

# Extract page title
page_title = soup.h1.get_text()
print(page_title)

# Extract lead
lead = soup.find(class_="lead").string
print(lead)

# Extract specific paragraph text and link from col-md-6 div
col_md_6 = soup.find('div', class_='col-md-6')
p_tag = col_md_6.find('p')
p_text_col_md_6 = p_tag.get_text(strip=True)
a_tag = p_tag.find('a')
a_text_col_md_6 = a_tag.get_text(strip=True)

print(f"Paragraph text: {p_text_col_md_6}")
print(f"Link text: {a_text_col_md_6}")

# Extract specific paragraph text and link from text-right div
text_right = soup.find('div', class_="text-right")
p_tag = text_right.find('p')
p_text_text_right = p_tag.get_text(strip=True)
a_tag = p_tag.find('a')
a_href_text_right = a_tag.get('href')

print(f"Paragraph text: {p_text_text_right}")
print(f"Link href: {a_href_text_right}")

# Extract all team data from the table
team_data_list = []
table = soup.find('table', class_='table')
# Iterate over each row in the table, skipping the header
for row in table.find_all('tr')[1:]:
    cells = row.find_all('td')
    team_data = {
        'Team Name': cells[0].get_text(strip=True),
        'Year': cells[1].get_text(strip=True),
        'Wins': cells[2].get_text(strip=True),
        'Losses': cells[3].get_text(strip=True),
        'OT Losses': cells[4].get_text(strip=True) or '0',  # Handle empty cells
        'Win %': cells[5].get_text(strip=True),
        'Goals For (GF)': cells[6].get_text(strip=True),
        'Goals Against (GA)': cells[7].get_text(strip=True),
        '+ / -': cells[8].get_text(strip=True)
    }
    team_data_list.append(team_data)

# Print the team data
for item in team_data_list:
    print(item)

# Load MongoDB credentials from environment variables
username = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")
cluster_url = os.getenv("MONGODB_CLUSTER_URL")

# Construct the MongoDB URI
mongo_uri = f"mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority"
client = pymongo.MongoClient(mongo_uri)

# Select the database and collection
db = client["Vakildesk_internship"]
collection = db["hockey_scraped_data"]

# Consolidate all the extracted data into a single dictionary
data_to_insert = {
    'title': title,
    'nav_links': nav_links,
    'page_title': page_title,
    'lead': lead,
    'paragraph_col_md_6': {
        'text': p_text_col_md_6,
        'link_text': a_text_col_md_6,
    },
    'paragraph_text_right': {
        'text': p_text_text_right,
        'link_href': a_href_text_right,
    },
    'team_data': team_data_list
}

# Insert the consolidated data into MongoDB
collection.insert_one(data_to_insert)
print("Data successfully inserted into MongoDB!")
