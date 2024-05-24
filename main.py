import requests
import os

def fileSave(url, path):
    try:
        r = requests.get(url)
        r.raise_for_status() 
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, "w", encoding='utf-8') as f:
            f.write(r.text)
            
        print(f"Content successfully saved to {path}")
        
    except requests.exceptions.RequestException as e:
        # Handle any requests-related errors
        print(f"An error occurred while fetching the URL: {e}")
    except OSError as e:
        # Handle file-related errors
        print(f"An error occurred while writing to the file: {e}")

url = "https://www.scrapethissite.com/pages/ajax-javascript/#2010"
fileSave(url, 'VakilDesk-Internship-Assignment/op.html')