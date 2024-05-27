from bs4 import BeautifulSoup

with open('content.html',"r") as f:
    html_doc = f.read()

soup = BeautifulSoup(html_doc, 'html.parser')
title = soup.title.string
nav_links = [link.get_text() for link in soup.find_all(class_="nav-link")]
page_title = soup.h3.get_text() if soup.h3 else "No page title"
lead = soup.find(class_="lead").string if soup.find(class_="lead") else "No lead"
links = soup.find_all('h4')
for link in links:
    a_tag = link.find('a')
    if a_tag:
        link_text = a_tag.text
        link_href = a_tag['href']
        print(f"Link text: {link_text}, Link href: {link_href}")

footer = soup.find(id="footer").text
print(title)
print(nav_links)
print(page_title)
print(lead)
print(footer)