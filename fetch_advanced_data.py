# import requests
import time
from bs4 import BeautifulSoup
# import os
# import gzip
# url = 'https://www.scrapethissite.com/pages/advanced/?gotcha=headers'
# headers = {
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#     'Referer': 'https://google.com',
#     'X-Forwarded-For': '192.168.1.1', 
#     # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
#     'X-Requested-With':'XMLHttpRequest',
#     # 'authority':'www.scrapethissite.com',
#     # 'scheme': 'https',
#     'Accept': 'text/html',
#     'Accept-Encoding': 'gzip, deflate, br, zstd',
#     'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
#     # 'Content-Length': '0',
#     # 'Cookie': 'ar_debug=1',
#     # 'Origin': 'https://www.scrapethissite.com',
#     # 'Priority': 'u=4, i',
#     # 'Referer': 'https://www.scrapethissite.com/',
#     # 'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
#     # 'Sec-Ch-Ua-Mobile': '?0',
#     # 'Sec-Ch-Ua-Platform': '"Windows"',
#     # 'Sec-Fetch-Dest': 'empty',
#     # 'Sec-Fetch-Mode': 'no-cors',
#     # 'Sec-Fetch-Site': 'cross-site',
# }

# r = requests.get(url, headers=headers)

# if r.headers.get('content-encoding')=='gzip':
#         # Decompress the gzip content
#     content = gzip.decompress(r.content)
# else:
#     content = r.content

#     # Decode the content using UTF-8 encoding
#     decoded_content = content.decode('windows-1252')

#     # Print the decoded content
#     # print(decoded_content)  

# print(r.text.encode('utf-8'))
# content_type = r.headers.get('content-type')
# print("Content-Type:", content_type)

# path = 'D:\VakilDesk\op3\op.html'
# r = requests.get(url,headers=headers)
# # r.raise_for_status()      
# os.makedirs(os.path.dirname(path), exist_ok=True)

# with open(path, "w", encoding='utf-8') as f:
#     f.write(r.text)
            
# print(f"Content successfully saved to {path}")


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Set the path to your Chrome WebDriver executable
url = 'https://www.scrapethissite.com/pages/advanced/?'
driver = webdriver.Chrome()

driver.get(url)
content = driver.page_source

with open('content.html', 'w', encoding='utf-8') as file:
    file.write(content)
    print(f"Content saved sucessfully!")

# # Find the 'Spoofing Headers' link and click on it
spoofing_headers_link = driver.find_element(By.XPATH, "//a[@href='/pages/advanced/?gotcha=headers']")
spoofing_headers_link.click()
time.sleep(2)

# Get the handles of all open tabs
handles = driver.window_handles

# Switch to the new tab 
driver.switch_to.window(handles[1])

spoofing_headers_content = driver.page_source

# Perform actions in the new tab
print("New tab URL:", driver.current_url)
# Extract the content of the 'Spoofing Headers' page
with open('spoofing_headers_content.html', 'w', encoding='utf-8') as file:
    file.write(spoofing_headers_content)
    print(f"spoofing_headers_content saved sucessfully!")

# # Close the browser
driver.switch_to.window(handles[0])
time.sleep(2)

login_link = driver.find_element(By.XPATH, "//a[@href='/pages/advanced/?gotcha=login']")
login_link.click()
time.sleep(2)

handles = driver.window_handles

driver.switch_to.window(handles[2])

login_content = driver.page_source

print("New tab URL:", driver.current_url)

# # Write the content to a file
with open('login_content.html', 'w', encoding='utf-8') as file:
    file.write(login_content)
    print(f"LOG in Content saved sucessfully!")


driver.switch_to.window(handles[0])
time.sleep(2)

csrf_link = driver.find_element(By.XPATH, "//a[@href='/pages/advanced/?gotcha=csrf']")
csrf_link.click()
time.sleep(2)

handles = driver.window_handles

driver.switch_to.window(handles[3])

csrf_content = driver.page_source

print("New tab URL:", driver.current_url)

# # Write the content to a file
with open('csrf_content.html', 'w', encoding='utf-8') as file:
    file.write(csrf_content)
    print(f"csrf Content saved sucessfully!")


driver.quit()
