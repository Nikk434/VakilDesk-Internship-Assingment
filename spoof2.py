from bs4 import BeautifulSoup
import os
import pymongo
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv("D:/VakilDesk/cred/.env")

directory_path = "D:/VakilDesk/output_2"

# Load MongoDB credentials from environment variables
username = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")
cluster_url = os.getenv("MONGODB_CLUSTER_URL")

# Construct the MongoDB URI
mongo_uri = f"mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority"
try:
    client = pymongo.MongoClient(mongo_uri)
    db = client["Vakildesk_internship"]
    collection = db["advanced_scraped_data"]
except pymongo.errors.PyMongoError as e:
    print(f"Error connecting to MongoDB: {e}")
    exit(1)

def parse_main_content(file_path):
    with open(file_path, "r") as f:
        html_doc = f.read()
    soup = BeautifulSoup(html_doc, 'html.parser')

    title = soup.title.string if soup.title else "No title"
    nav_links = [link.get_text() for link in soup.find_all(class_="nav-link")]
    page_title = soup.h3.get_text() if soup.h3 else "No page title"
    lead = soup.find(class_="lead").string if soup.find(class_="lead") else "No lead"
    links = [(a_tag.text, a_tag['href']) for link in soup.find_all('h4') if (a_tag := link.find('a'))]
    footer = soup.find(id="footer").text if soup.find(id="footer") else "No footer"

    return {
        'type': 'main_content',
        'title': title,
        'nav_links': nav_links,
        'page_title': page_title,
        'lead': lead,
        'links': links,
        'footer': footer
    }

def parse_spoofing_headers_content(file_path):
    with open(file_path, "r") as f:
        html_doc = f.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    data = soup.find(class_="col-md-offset-4").string if soup.find(class_="col-md-offset-4") else "No data"
    return {'type': 'spoofing_headers_content', 'data': data}

def parse_login_content(file_path):
    with open(file_path, "r") as f:
        html_doc = f.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    data = soup.get_text()
    return {'type': 'login_content', 'data': data}

def parse_csrf_content(file_path):
    with open(file_path, "r") as f:
        html_doc = f.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    data = soup.get_text()
    return {'type': 'csrf_content', 'data': data}

# Parse and gather data from each file
all_data_to_insert = []
all_data_to_insert.append(parse_main_content('content.html'))
all_data_to_insert.append(parse_spoofing_headers_content('spoofing_headers_content.html'))
all_data_to_insert.append(parse_login_content('login_content.html'))
all_data_to_insert.append(parse_csrf_content('csrf_content.html'))

# Insert data into MongoDB
try:
    if all_data_to_insert:
        collection.insert_many(all_data_to_insert)
        print("Data successfully inserted into MongoDB!")
    else:
        print("No data to insert into MongoDB.")
except pymongo.errors.PyMongoError as e:
    print(f"Error inserting data into MongoDB: {e}")
