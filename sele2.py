from bs4 import BeautifulSoup
import os
import pymongo
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv("D:\VakilDesk\cred\.env")

directory_path = "D:\VakilDesk\output_2"

# Read the HTML file

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



def scrape_web_content():
    # Extract title
    title = soup.title.string

    # Extract nav elements
    nav = soup.find_all(class_="nav-link")
    nav_links = [link.get_text() for link in nav]
    for link in nav_links:
        pass

    # Extract page title
    page_title = soup.h1.get_text()

    # Extract lead
    lead = soup.find(class_="lead").string

    # Extract specific paragraph text and link from col-md-6 div
    col_md_6 = soup.find('div', class_='col-md-6')
    p_tag = col_md_6.find('p')
    p_text_col_md_6 = p_tag.get_text(strip=True)
    a_tag = p_tag.find('a')
    a_text_col_md_6 = a_tag.get_text(strip=True)


    # Extract specific paragraph text and link from text-right div
    text_right = soup.find('div', class_="text-right")
    p_tag = text_right.find('p')
    p_text_text_right = p_tag.get_text(strip=True)
    a_tag = p_tag.find('a')
    a_href_text_right = a_tag.get('href')


    return {
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
        }
    }

def scrape_team_data(soup):
    team_data_list = []
    table = soup.find('table', class_='table')
    # Iterate over each row in the table, skipping the header
    if table:
        for row in table.find_all('tr')[1:]:
            cells = row.find_all('td')
            if len(cells) == 9:
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
        pass
        # print(item)

    return team_data_list

all_data_to_insert = []

# Read the first file to scrape web content
first_file = os.listdir(directory_path)[0]
first_file_path = os.path.join(directory_path, first_file)
with open(first_file_path, "r", encoding="utf-8") as f:
    html_doc = f.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    # Scrape web content
    web_content_data = scrape_web_content()

all_data_to_insert.append(web_content_data)

# Iterate over each file in the directory to scrape team data
for filename in os.listdir(directory_path):
    if filename.endswith(".html"):
        file_path = os.path.join(directory_path, filename)
        print(filename,"\n")
        with open(file_path, "r", encoding="utf-8") as f:
            html_doc = f.read()
            soup = BeautifulSoup(html_doc, 'html.parser')
            # Scrape team data
            team_data_list = scrape_team_data(soup)

            # Consolidate all the extracted data into a single dictionary
            data_to_insert = {
                'team_data': team_data_list
            }

            # Add the data to the list
            all_data_to_insert.append(data_to_insert)

# Insert all the data into MongoDB at once
if all_data_to_insert:
    collection.insert_many(all_data_to_insert)
    print("Data successfully inserted into MongoDB!")
else:
    print("No data to insert into MongoDB.")
