import requests

def fileSave(url, path):
    r = requests.get(url)
    with open(path,"w") as f:
        f.write(r.text)

url= "https://www.scrapethissite.com/pages/ajax-javascript/#2010"

fileSave(url,'VakilDesk-Internship-Assingment/op.html')