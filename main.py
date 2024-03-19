import requests 
from bs4 import BeautifulSoup

url = 'https://www.nytimes.com/'
html = requests.get(url)
print(html.text)