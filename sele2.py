from bs4 import BeautifulSoup
import os

file_path = "D:\VakilDesk\output_2\page_1.html"
with open(file_path,"r") as f:
    html_doc = f.read()

soup = BeautifulSoup(html_doc, 'html.parser')
title = soup.title.string
#title
print(title)
#nav elements
nav = soup.find_all(class_="nav-link")
for link in nav:
    print(link.get_text())

#page_title
page_title = soup.h1.get_text()
print(page_title)

#lead
lead = soup.find(class_="lead").string
print(lead)

#get specific paragraph text and link 
col_md_6 = soup.find('div', class_='col-md-6')
p_tag = col_md_6.find('p')
p_text = p_tag.get_text()
a_tag = p_tag.find('a')
a_text = a_tag.get_text()

print(f"Paragraph text: {p_text}")
print(f"Link text: {a_text}")

#get specific paragraph text and link 
text_right = soup.find('div', class_="text-right")
p_tag = text_right.find('p')
p_text = p_tag.get_text()
a_tag = p_tag.find('a')
a_href = a_tag.get_text()

print(f"Paragraph text: {p_text}")
print(f"Link href: {a_href}")

#get all team data 
data = []
table = soup.find('table', class_='table')
# Iterate over each row in the table, skipping the header
for row in table.find_all('tr')[1:]:
    cells = row.find_all('td')
    team_data = {
        'Team Name': cells[0].get_text(strip=True),
        'Year': cells[1].get_text(strip=True),
        'Wins': cells[2].get_text(strip=True),
        'Losses': cells[3].get_text(strip=True),
        'OT Losses': cells[4].get_text(strip=True) or '0',  # Handle empty cells
        'Win %': cells[5].get_text(strip=True),
        'Goals For (GF)': cells[6].get_text(strip=True),
        'Goals Against (GA)': cells[7].get_text(strip=True),
        '+ / -': cells[8].get_text(strip=True)
    }
    data.append(team_data)

# Print the data
for item in data:
    print(item)