import os
from selenium import webdriver
from selenium.webdriver.common.by import By

url_template = 'https://www.scrapethissite.com/pages/forms/?page_num={}'

# Initialize the Chrome webdriver
driver = webdriver.Chrome()

# # Function to get all links on a page
# def get_links():
#     return driver.find_elements(By.TAG_NAME, 'a')

# Function to save HTML content to a file
def save_html_content(content, folder_path, file_name):
    try:
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, file_name)

        with open(file_path, "w", encoding='utf-8') as f:
            f.write(content)

        print(f"Content successfully saved to {file_path}")

    except OSError as e:
        print(f"An error occurred while writing to the file: {e}")


# Function to visit each page and save HTML content
def visit_pages(page_numbers):
    folder_path = 'D:\VakilDesk\output_2'  # Specify the folder path where you want to save HTML files
    for page_number in page_numbers:
        url = url_template.format(page_number)
        try:
            driver.get(url)
            print("Visited page:", page_number)
            html_content = driver.page_source  # Get the HTML content of the current page
            file_name = f"page_{page_number}.html"
            save_html_content(html_content, folder_path, file_name)  # Save HTML content to the specified folder
        except Exception as e:
            print("Error visiting page:", page_number)
            print(e)

start_page = 1
end_page = 24
page_numbers = range(start_page, end_page + 1)

# Visit each page and save HTML content to a single file
visit_pages(page_numbers)

# Close the webdriver
driver.quit()
