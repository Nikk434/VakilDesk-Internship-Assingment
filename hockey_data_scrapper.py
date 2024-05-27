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
    collection = db["hockey_scraped_data"]
except pymongo.errors.PyMongoError as e:
    print(f"Error connecting to MongoDB: {e}")
    exit(1)

def scrape_web_content(soup):
    try:
        title = soup.title.string if soup.title else "No title"
        nav_links = [link.get_text() for link in soup.find_all(class_="nav-link")]
        page_title = soup.h1.get_text() if soup.h1 else "No page title"
        lead = soup.find(class_="lead").string if soup.find(class_="lead") else "No lead"

        col_md_6 = soup.find('div', class_='col-md-6')
        if col_md_6:
            p_tag = col_md_6.find('p')
            p_text_col_md_6 = p_tag.get_text(strip=True) if p_tag else "No text"
            a_tag = p_tag.find('a') if p_tag else None
            a_text_col_md_6 = a_tag.get_text(strip=True) if a_tag else "No link text"
        else:
            p_text_col_md_6, a_text_col_md_6 = "No text", "No link text"

        text_right = soup.find('div', class_="text-right")
        if text_right:
            p_tag = text_right.find('p')
            p_text_text_right = p_tag.get_text(strip=True) if p_tag else "No text"
            a_tag = p_tag.find('a') if p_tag else None
            a_href_text_right = a_tag.get('href') if a_tag else "No link"
        else:
            p_text_text_right, a_href_text_right = "No text", "No link"

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
    except Exception as e:
        print(f"Error scraping web content: {e}")
        return {}

def scrape_team_data(soup):
    team_data_list = []
    try:
        table = soup.find('table', class_='table')
        if table:
            for row in table.find_all('tr')[1:]:
                cells = row.find_all('td')
                if len(cells) == 9:
                    team_data = {
                        'Team Name': cells[0].get_text(strip=True),
                        'Year': cells[1].get_text(strip=True),
                        'Wins': cells[2].get_text(strip=True),
                        'Losses': cells[3].get_text(strip=True),
                        'OT Losses': cells[4].get_text(strip=True) or '0',
                        'Win %': cells[5].get_text(strip=True),
                        'Goals For (GF)': cells[6].get_text(strip=True),
                        'Goals Against (GA)': cells[7].get_text(strip=True),
                        '+ / -': cells[8].get_text(strip=True)
                    }
                    team_data_list.append(team_data)
    except Exception as e:
        print(f"Error scraping team data: {e}")
    return team_data_list

all_data_to_insert = []

try:
    first_file = os.listdir(directory_path)[0]
    first_file_path = os.path.join(directory_path, first_file)
    with open(first_file_path, "r", encoding="utf-8") as f:
        html_doc = f.read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        web_content_data = scrape_web_content(soup)
    all_data_to_insert.append(web_content_data)
except IndexError:
    print("No files found in the directory.")
    exit(1)
except Exception as e:
    print(f"Error processing the first file: {e}")
    exit(1)

try:
    for filename in os.listdir(directory_path):
        if filename.endswith(".html"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                html_doc = f.read()
                soup = BeautifulSoup(html_doc, 'html.parser')
                team_data_list = scrape_team_data(soup)
                data_to_insert = {'team_data': team_data_list}
                all_data_to_insert.append(data_to_insert)
except Exception as e:
    print(f"Error processing files: {e}")

try:
    if all_data_to_insert:
        collection.insert_many(all_data_to_insert)
        print("Data successfully inserted into MongoDB!")
    else:
        print("No data to insert into MongoDB.")
except pymongo.errors.PyMongoError as e:
    print(f"Error inserting data into MongoDB: {e}")
