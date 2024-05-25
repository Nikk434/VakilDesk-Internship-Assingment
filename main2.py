from bs4 import BeautifulSoup
import pymongo
from dotenv import load_dotenv
import os
import string

load_dotenv("D:\VakilDesk\cred\.env")

with open("output_1\op.html","r") as f:
    html_doc = f.read()

soup = BeautifulSoup(html_doc, 'html.parser')

all_content = soup.get_text()
text = all_content.strip(string.whitespace)
print(text)

username = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")
cluster_url = os.getenv("MONGODB_CLUSTER_URL")

# Construct the MongoDB URI
mongo_uri = f"mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority"
client = pymongo.MongoClient(mongo_uri)


db = client["Vakildesk_internship"]
collection = db["films_scraped_content"]

document = {
    "content": all_content
}

# Insert the document into the collection
collection.insert_one(document)

print("Content stored in MongoDB successfully.")
