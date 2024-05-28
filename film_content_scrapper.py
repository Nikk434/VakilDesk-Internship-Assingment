import requests
import json
import os
import pymongo
from dotenv import load_dotenv
load_dotenv("D:\VakilDesk\cred\.env")

# Function to save HTML content to a file with exception handling
def fileSave(url, path):
    try:
        r = requests.get(url)
        r.raise_for_status()  
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, "w", encoding='utf-8') as f:
            f.write(r.text)
            
        print(f"Content successfully saved to {path}")
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the URL: {e}")
    except OSError as e:
        print(f"An error occurred while writing to the file: {e}")

# Function to fetch film data and handle exceptions
def fetch_film_data(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()  
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve data from {url}: {e}")
        return None

html_url = "https://www.scrapethissite.com/pages/ajax-javascript/#2010" #url for static content 
html_path = 'output_1/op.html'
fileSave(html_url, html_path)

# Define the years 
years = [2010, 2011, 2012, 2013, 2014, 2015]
base_url = "https://www.scrapethissite.com/pages/ajax-javascript/?ajax=true&year=" #url for dynamic content 

output_dir = 'output_1/films_data'
os.makedirs(output_dir, exist_ok=True)

# Dictionary to hold all the data
all_data = {}

# Fetch data for each year and store it in the dictionary
for year in years:
    url = f"{base_url}{year}"
    data = fetch_film_data(url)
    if data is not None:
        all_data[year] = data

output_file_path = os.path.join(output_dir, "all_films.json")

# Save the data to the single JSON file
try:
    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4)
    print(f"All data saved successfully to {output_file_path}")
except OSError as e:
    print(f"An error occurred while writing to the JSON file: {e}")

# Function to save scraped data in mongobd 
def storeIN_mongodb():
    username = os.getenv("MONGODB_USERNAME")
    password = os.getenv("MONGODB_PASSWORD")
    cluster_url = os.getenv("MONGODB_CLUSTER_URL")


    # Construct the MongoDB URI
    mongo_uri = f"mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority"

    client = pymongo.MongoClient(mongo_uri)
    db = client["Vakildesk_internship"]
    collection = db["films_scraped_data"]

    file_path = r'D:\VakilDesk\output_1\films_data\all_films.json'

    try:
        with open(file_path, 'r') as file:
            file_data = json.load(file)

        if isinstance(file_data, list):
            collection.insert_many(file_data)
        else:
            collection.insert_one(file_data)

        print("Data inserted successfully")

    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file at {file_path}.")
    except pymongo.errors.PyMongoError as e:
        print(f"An error occurred while inserting data into MongoDB: {e}")

storeIN_mongodb()
