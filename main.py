import requests 
from bs4 import BeautifulSoup

url = 'https://www.opb.org/'
html = requests.get(url)

if html.status_code == 200:
    soup = BeautifulSoup(html.content, 'html.parser')
    story_cards = soup.find_all(class_='story-card story-card__vert color_dgray width_full lead_media')  # Find all elements with class 'story-card story-card__vert color_dgray width_full lead_media'

    if story_cards:
        for card in story_cards:
            story_link = card.find('a')['href']
            print("Link:", story_link)
    else:
        print("No elements with class 'story-card story-card__vert color_dgray width_full lead_media' found.")
else:
    print("Failed to retrieve webpage. Status code:", html.status_code)



# to see scrap data
#print(html.text)
