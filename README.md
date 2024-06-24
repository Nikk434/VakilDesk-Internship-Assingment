# Web Scrapping 

A brief overview of the project.

## Necessary Libraries

- request
- BeautifulSoup
- pymongo
- os
- selenium
- time
- json
- string

To install these libraries, use `pip install library_name`.

## MongoDB Atlas Setup

For setting up MongoDB Atlas, follow the steps outlined in [this video tutorial](https://youtu.be/iA51dgWq4Ok?si=YD6luAgzv37Xw1Mn). 

1. Create a `.env` file to store your MongoDB credentials.
2. Load this file to pass your credentials as placeholders.

Example:
MONGODB_USERNAME=your_username
MONGODB_PASSWORD=your_password
MONGODB_CLUSTER_URL=your_cluster_url

_Note: Edit the path/filename/directory name as per your preferences._

## First Website - Oscar Winning Films

![Oscar Winning Films](https://github.com/Nikk434/VakilDesk-Internship-Assingment/assets/159627869/bdabfeb9-2c7e-4e54-bf29-33997ca8f519)

The first website displays a list of Oscar-winning films from 2010 to 2015. Users need to click on a year to view the films for that specific year. The film data is dynamically loaded using an API.

### Scraping Process
1. **Locate API:** Follow the steps outlined to find the API URL.
- On website Left click or Ctrl + Shift + I
- Go to Networks tab
- Reload the page
- Look for the requests that match the type of API call you are interested in (e.g., GET, POST, PUT, DELETE).
- Click on a request to see its details.
- You can copy the URL of the API 
2. **Run Scripts:** Execute `film_content_scrapper.py` and `film_data_scrapper.py` to save and scrape the data respectively.

## Second Website - Hockey Teams Data

![Hockey Teams Data](https://github.com/Nikk434/VakilDesk-Internship-Assingment/assets/159627869/c2a75035-c125-4d63-a8b1-e858d45665bb)

Similar to the first website, this website displays hockey teams' data from pages 1 to 25, with each page containing 25 entries. The data is static and embedded into the frontend of each page.

### Scraping Process
1. **Run Scripts:** Execute `fetch_hockey_data.py` and `hockey_data_scrapper.py` to scrape and store the data respectively.

## Third Website - Advanced Scenarios

This website presents three links, each requiring user interaction for access.

### Scraping Process
1. **Utilize Selenium:** Use Selenium to interact with the website.
2. **Run Scripts:** Execute `fetch_advanced_data.py` and `advanced_data_scrapper.py` to scrape and store the data respectively.

## Data Storage in MongoDB

![MongoDB Data](https://github.com/Nikk434/VakilDesk-Internship-Assingment/assets/159627869/4ed3fbef-06af-46b0-92dc-e11228eb94c2)
![More MongoDB Data](https://github.com/Nikk434/VakilDesk-Internship-Assingment/assets/159627869/12d3daa5-0639-46a1-adb9-a6f48c0a1ded)
