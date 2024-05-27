from bs4 import BeautifulSoup
import pymongo
from dotenv import load_dotenv
import os
import string

try:
    load_dotenv("D:\VakilDesk\cred\.env")
except Exception as e:
    print(f"Error loading .env file: {e}")

try:
    with open("output_1\op.html", "r") as f:
        html_doc = f.read()
except Exception as e:
    print(f"Error reading HTML file: {e}")
    # Handle the error here, maybe exit the program or try an alternative approach

try:
    soup = BeautifulSoup(html_doc, 'html.parser')
    all_content = soup.get_text()
    text = all_content.strip(string.whitespace)
except Exception as e:
    print(f"Error processing HTML content: {e}")
    # Handle the error here, maybe exit the program or try an alternative approach

try:
    username = os.getenv("MONGODB_USERNAME")
    password = os.getenv("MONGODB_PASSWORD")
    cluster_url = os.getenv("MONGODB_CLUSTER_URL")

    # Construct the MongoDB URI
    mongo_uri = f"mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(mongo_uri)
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    # Handle the error here, maybe exit the program or try an alternative approach

try:
    db = client["Vakildesk_internship"]
    collection = db["films_scraped_content"]

    document = {
        "content": all_content
    }

    # Insert the document into the collection
    collection.insert_one(document)
    print("Content stored in MongoDB successfully.")
except Exception as e:
    print(f"Error storing content in MongoDB: {e}")
    # Handle the error here, maybe exit the program or try an alternative approach
